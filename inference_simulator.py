#!/usr/bin/env python3
"""
Simulate inferred `situation:requiresPractice` assertions from local RDF/XML files.
Usage: python3 inference_simulator.py [--out out.rdf]

No external deps — uses xml.etree.ElementTree only.
"""
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent
FILES = ["Situation.rdf","crop.rdf","Practice.rdf","Nutriment.rdf","Soil.rdf","climate.rdf"]

def local(tag):
    if '}' in tag:
        return tag.split('}',1)[1]
    return tag

# parse files
triples = defaultdict(list)   # subj -> list of (pred_local, obj)
literals = defaultdict(list)  # subj -> list of (pred_local, text)

for fname in FILES:
    f = BASE / fname
    if not f.exists():
        continue
    tree = ET.parse(str(f))
    root = tree.getroot()
    for desc in root.findall('.//'):
        about = desc.attrib.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about')
        if about:
            subj = about
            for child in list(desc):
                tag = local(child.tag)
                res = child.attrib.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource')
                if res:
                    triples[subj].append((tag,res))
                else:
                    text = (child.text or '').strip()
                    if text!='':
                        literals[subj].append((tag,text))

# Build crop requirements: crop -> {NutrientName: minValue}
crop_reqs = defaultdict(dict)
for subj, props in triples.items():
    for (p,o) in props:
        if p=='hasNutrientRequirement':
            req = o
            # find nutrient (object triple concernsNutrient)
            nut = None
            for (pp,oo) in triples.get(req,[]):
                if pp.endswith('concernsNutrient') or pp=='concernsNutrient':
                    nut = oo.split('#')[-1]
            # find min
            minv = None
            for (tag,val) in literals.get(req,[]):
                if tag.endswith('hasMinRequirement') or tag=='hasMinRequirement':
                    try:
                        minv = float(val)
                    except:
                        minv = None
            if nut and minv is not None:
                crop_reqs[subj][nut] = minv

# practice defaults (IRIs)
PRACTICE_NS = 'http://www.semanticweb.org/megnastephane/ontologies/2026/3/practice#'
practice_defaults = {
    'Nitrogen': PRACTICE_NS + 'NitrogenFertilization_Default',
    'Phosphorus': PRACTICE_NS + 'PhosphorusFertilization_Default',
    'Potassium': PRACTICE_NS + 'PotassiumFertilization_Default',
    'Irrigation': PRACTICE_NS + 'Irrigation_Default'
}

# nutrient -> soil property name
soil_props = {
    'Nitrogen':'hasNitrogenLevel',
    'Phosphorus':'hasPhosphorusLevel',
    'Potassium':'hasPotassiumLevel'
}

# find AgriculturalSituation subjects
AGRI_TYPE = 'http://www.semanticweb.org/megnastephane/ontologies/2026/3/situation#AgriculturalSituation'
situations = []
for subj, props in triples.items():
    for (p,o) in props:
        if (p=='type' or p.endswith('type')) and o==AGRI_TYPE:
            situations.append(subj)

report = []
for s in situations:
    inferred = set()
    soils = [o for (p,o) in triples.get(s,[]) if p.endswith('hasSoil') or p=='hasSoil']
    crops = [o for (p,o) in triples.get(s,[]) if p.endswith('hasCrop') or p=='hasCrop']
    clims = [o for (p,o) in triples.get(s,[]) if p.endswith('hasClimate') or p=='hasClimate']
    soil_res = soils[0] if soils else None
    crop_res = crops[0] if crops else None
    cl_res = clims[0] if clims else None

    # climate check: if climate IRI contains 'Unfavorable' or class 'UnfavorableClimate' appears
    if cl_res:
        if 'Unfavorable' in cl_res or cl_res.endswith('UnfavorableClimate'):
            inferred.add(practice_defaults['Irrigation'])
        else:
            # check triples of the climate resource for rdf:type that endswith UnfavorableClimate
            for (p,o) in triples.get(cl_res,[]):
                if (p=='type' or p.endswith('type')) and ('UnfavorableClimate' in o or o.endswith('UnfavorableClimate')):
                    inferred.add(practice_defaults['Irrigation'])

    # nutrients
    for nutrient, soilprop in soil_props.items():
        if not soil_res or not crop_res:
            continue
        lvls = [o for (p,o) in triples.get(soil_res,[]) if p==soilprop or p.endswith(soilprop)]
        if not lvls:
            continue
        lvl = lvls[0]
        val = None
        for (tag,v) in literals.get(lvl,[]):
            if tag=='hasValue' or tag.endswith('hasValue'):
                try:
                    val = float(v)
                except:
                    val = None
        mins = None
        # crop_reqs keyed by crop subject
        reqs = crop_reqs.get(crop_res, {})
        mins = reqs.get(nutrient)
        if val is not None and mins is not None and val < mins:
            # map nutrient to practice
            piri = practice_defaults.get(nutrient)
            if piri:
                inferred.add(piri)
    report.append((s, inferred))

# print report
for s, inf in report:
    print('Situation:', s)
    if inf:
        for p in sorted(inf):
            print('  -> inferred:', p)
    else:
        print('  -> no inferred practice')

# optional write-out
if '--out' in sys.argv:
    try:
        idx = sys.argv.index('--out')
        outpath = sys.argv[idx+1]
    except Exception:
        outpath = 'inferred_practices.rdf'
    # build simple RDF/XML with requiresPractice assertions
    ns = {
        'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'situation':'http://www.semanticweb.org/megnastephane/ontologies/2026/3/situation#',
        'practice':'http://www.semanticweb.org/megnastephane/ontologies/2026/3/practice#'
    }
    ET.register_namespace('', ns['situation'])
    ET.register_namespace('rdf', ns['rdf'])
    ET.register_namespace('practice', ns['practice'])
    root = ET.Element('{%s}RDF' % ns['rdf'])
    for s,inf in report:
        if not inf:
            continue
        desc = ET.SubElement(root, '{%s}Description' % ns['rdf'], { '{%s}about' % ns['rdf']: s })
        for p in sorted(inf):
            # create requiresPractice element in situation namespace
            el = ET.SubElement(desc, '{%s}requiresPractice' % ns['situation'])
            el.set('{%s}resource' % ns['rdf'], p)
    tree = ET.ElementTree(root)
    tree.write(outpath, encoding='utf-8', xml_declaration=True)
    print('\nWritten inferred assertions to', outpath)
