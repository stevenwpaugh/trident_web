from django import template

register = template.Library()

@register.simple_tag
def complement(seq):
        basecomplement = {'-':'-', 'u':'a', 'U':'A', 'a':'t', 'c':'g', 't':'a', 'g':'c', 'A':'T', 'C':'G', 'T':'A', 'G':'C', 'n':'n', 'N':'N'}
        letters = list (seq)
        dna = ''
        for base in letters:
                dna += basecomplement[base]
        return dna

@register.filter
def keyvalue(dict, key):
	return dict[key]

@register.filter
def genename(genes, name):
	gene = genes[name]
	if not gene:
		return ""
	else:
		return gene.name
	

@register.filter
def genencbi(genes, name):
	import re
	gene = genes[name]
	if not gene:
		return ""
	db_xref = gene.db_xref
	if not db_xref or not "GeneID" in db_xref:
		return ""
	m = re.search("GeneID:([^,]*),",db_xref)
	if m and m.groups():
		return m.groups()[0]

@register.filter
def commafy(string, replaced):
	return string.replace(replaced,",")

@register.filter
def getgrade(result):
	from ple.views import get_interpolator, get_grade
	if not result:
		return None
	interp = get_interpolator()
	if interp:
		return get_grade(interp(result["energy"],result["score"]))
