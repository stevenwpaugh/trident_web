#!/usr/bin/env python
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trident_web.settings")

from django.core.management import execute_from_command_line
from tridentdb.models import Results

def results_to_gff(file, mirna_name):
    file.write("##gff-version 3\n")
    for result in Results.objects.filter(microrna = mirna_name):
        file.write("%s\n" % result.gff())


def write_all_micrornas():
    for mirna_names in Results.objects.distinct('microrna'):
        with open("%s.gff" % mirna_names.microrna,"w") as file:
            results_to_gff(file,mirna_names.microrna)


if __name__ == "__main__":
    from sys import argv
    if len(argv) > 1 and ("help" in argv[1] or argv[1] == "-h"):
        print("./exporter.py")
        print("\nWrites GFF files for each micro RNA, containing hits against all genomes in the database.")
        exit(0)

    write_all_micrornas()


