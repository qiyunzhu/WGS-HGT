# ----------------------------------------------------------------------------
# Copyright (c) 2015--, The WGS-HGT Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

"""
Reformat input genome files to formats required by given
GI tool
=========================================================
"""

import click
from os import remove
from os.path import join

from skbio import Sequence, DNA


def reformat_egid(genbank_fp,
                  output_dir):
    """ Reformat input genome to the formats accepted by EGID.

    Parameters
    ----------
    genbank_fp: string
        file path to genome in GenBank format
    output_dir: string
        output directory path

    Notes
    -----
    Input to EGID are five obsolete NCBI standard files: gbk, fna, faa, ffn
    and ptt.
    """
    loci = []
    nucl_seq = ''
    genes = {}
    nseq = 0  # number of nucleotide sequences
    with open(genbank_fp, 'r') as input_f:
        for line in input_f:
            if line.startswith('//'):
                nseq += 1
    abs_pos = 0  # absolute position in concantenated nucleotide sequence
    for i in range(nseq):
        gb = Sequence.read(genbank_fp, seq_num=i+1, format='genbank')
        locus_name = gb.metadata['LOCUS']['locus_name']
        size = gb.metadata['LOCUS']['size']
        loci.append([locus_name, size])
        nucl_seq += str(gb)
        for feature in gb.interval_metadata.features:
            if feature['type_'] == 'CDS' and 'protein_id' in feature:
                protein_id = feature['protein_id'].replace('\"', '')
                if protein_id not in genes:
                    translation = feature['translation'].replace(' ', '') \
                        .replace('\"', '')
                    strand = '-' if feature['rc_'] else '+'
                    loc = gb.interval_metadata.features[feature]
                    start = loc[0][0] + abs_pos + 1
                    end = loc[0][1] + abs_pos
                    genes[protein_id] = [translation, start, end, strand]
        abs_pos += int(size)
    output_f = {}
    for x in ('fna', 'faa', 'ffn', 'ptt', 'gbk'):
        output_f[x] = open(join(output_dir, 'id.' + x), 'w')
    gb = DNA(nucl_seq)
    gb.metadata['LOCUS'] = {'locus_name': 'locus001', 'size': len(nucl_seq),
                            'unit': 'bp', 'shape': 'circular',
                            'division': 'CON', 'mol_type': 'DNA',
                            'date': '01-JAN-1900'}
    tmp_fp = join(output_dir, 'id.tmp')
    DNA.write(gb, tmp_fp, format='genbank')
    with open(tmp_fp, 'r') as input_f:
        output_f['gbk'].write(input_f.readline())
    output_f['gbk'].write('FEATURES             Location/Qualifiers\n')
    output_f['ptt'].write('locus001\n' + str(len(genes)) + ' proteins\n')
    fields = ('Location', 'Strand', 'Length', 'PID', 'Gene', 'Synonym',
              'Code', 'COG', 'Product')
    output_f['ptt'].write('\t'.join(fields) + '\n')
    output_f['fna'].write('>locus001\n' + nucl_seq + '\n')
    gid = 1
    for (gene, l) in sorted(genes.items(), key=lambda x: x[1][1]):
        output_f['faa'].write('>' + gene + '\n' + l[0] + '\n')
        output_f['ptt'].write(str(l[1]) + '..' + str(l[2]) + '\t' +
                              l[3] + '\t' + str(len(l[0])) + '\t' +
                              str(gid) + '\t-\tgene' + str(gid) +
                              '\t-\t-\t-\n')
        if l[3] == '+':
            output_f['ffn'].write('>locus001:' + str(l[1]) + '-' +
                                  str(l[2]) + '\n' +
                                  nucl_seq[l[1]-1:l[2]] + '\n')
        else:
            rc_seq = str(DNA(nucl_seq[l[1]-1:l[2]]).reverse_complement())
            output_f['ffn'].write('>locus001:c' + str(l[2]) + '-' +
                                  str(l[1]) + '\n' + rc_seq + '\n')
        location = str(l[1]) + '..' + str(l[2])
        if l[3] == '-':
            location = 'complement(' + location + ')'
        lines = []
        lines.append('     gene            ' + location)
        lines.append('                     /locus_tag=gene' + str(gid))
        lines.append('     CDS             ' + location)
        lines.append('                     /locus_tag=gene' + str(gid))
        lines.append('                     /protein_id=' + gene)
        lines.append('                     /translation=' + l[0])
        for line in lines:
            output_f['gbk'].write(line + '\n')
        gid += 1
    with open(tmp_fp, 'r') as input_f:
        next(input_f)
        for line in input_f:
            output_f['gbk'].write(line)
    for x in output_f:
        output_f[x].close()
    remove(tmp_fp)


@click.command()
@click.option('--genbank-fp', required=True,
              type=click.Path(resolve_path=True, readable=True, exists=True,
                              file_okay=True),
              help='Genome in GenBank format')
@click.option('--output-dir', required=True,
              type=click.Path(resolve_path=True, readable=True, exists=False),
              help='Output directory path')
@click.option('--method', required=True,
              type=click.Choice(['egid', 'genemark']),
              help='The method to be used for GI detection')
def _main(genbank_fp,
          output_dir,
          method):
    """ Reformat genome files
    """
    if method == 'egid':
        reformat_egid(
            genbank_fp=genbank_fp,
            output_dir=output_dir)


if __name__ == "__main__":
    _main()