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
