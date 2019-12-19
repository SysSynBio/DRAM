#!/usr/bin/env python3

import argparse

from mag_annotator.database_processing import prepare_databases, set_database_paths, print_database_locations,\
                                              populate_description_db
from mag_annotator.annotate_vgfs import annotate_vgfs
from mag_annotator.summarize_vgfs import summarize_vgfs
from mag_annotator.pull_sequences import pull_sequences

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    subparsers = parser.add_subparsers()
    prepare_dbs_parser = subparsers.add_parser('prepare_databases',
                                               help="Download and process databases for annotation",
                                               formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    set_db_locs_parser = subparsers.add_parser('set_database_locations',
                                               help="Set database locations for already processed databases",
                                               formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    update_description_db_parser = subparsers.add_parser('update_description_db', help='Update description database',
                                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    print_db_locs_parser = subparsers.add_parser('print_config', help="Print database locations",
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    annotate_parser = subparsers.add_parser('annotate', help="Annotate viral contigs",
                                            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    distill_parser = subparsers.add_parser('distill',
                                           help="Summarize AMGs in annotated viral genome fragments",
                                           formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    strainer_parser = subparsers.add_parser('strainer', help="Strain annotations down to genes of interest",
                                            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # parser for downloading and processing databases for annotation and summarization
    prepare_dbs_parser.add_argument('--output_dir', default="~/DRAM_data", help="output directory")
    prepare_dbs_parser.add_argument('--kegg_loc', default=None,
                                    help="KEGG protein file, should be a single .pep, please merge all KEGG pep files")
    prepare_dbs_parser.add_argument('--gene_ko_link_loc', default=None,
                                    help="KEGG gene ko link, can be gzipped or not")
    prepare_dbs_parser.add_argument('--kegg_download_date', default=None,
                                    help="Date KEGG was download to include in database name")
    prepare_dbs_parser.add_argument('--uniref_loc', default=None, help="File path to uniref, if already downloaded")
    prepare_dbs_parser.add_argument('--uniref_version', default='90', help="UniRef version to download")
    prepare_dbs_parser.add_argument('--pfam_loc', default=None,
                                    help="File path to pfam-A hmm file, if already downloaded")
    prepare_dbs_parser.add_argument('--pfam_hmm_dat', default=None, help="pfam hmm .dat file to get PF"
                                                                         "descriptions, if already downloaded")
    prepare_dbs_parser.add_argument('--pfam_release', default='32.0', help="Pfam release to download")
    prepare_dbs_parser.add_argument('--dbcan_loc', default=None, help="File path to dbCAN, if already downloaded")
    prepare_dbs_parser.add_argument('--dbcan_fam_activities', default=None, help='CAZY family activities file, if'
                                                                                 'already downloaded')
    prepare_dbs_parser.add_argument('--dbcan_version', default='7', type=str, help='version of dbCAN to use')
    prepare_dbs_parser.add_argument('--vogdb_loc', default=None, help='hmm file for vogdb, if already downloaded')
    prepare_dbs_parser.add_argument('--viral_loc', default=None,
                                    help="File path to viral protein faa, if already downloaded")
    prepare_dbs_parser.add_argument('--peptidase_loc', default=None,
                                    help="File path to MEROPS peptidase fasta, if already downloaded")
    prepare_dbs_parser.add_argument('--genome_summary_form_loc', default=None, help="File path to genome summary form,"
                                                                                    "if already downloaded")
    prepare_dbs_parser.add_argument('--module_step_form_loc', default=None, help="File path to module step form, if"
                                                                                 "already downloaded")
    prepare_dbs_parser.add_argument('--etc_module_database_loc', default=None,
                                    help="File path to etc module database, if already downloaded")
    prepare_dbs_parser.add_argument('--function_heatmap_form_loc', default=None,
                                    help="File path to function heatmap form, if already downloaded")
    prepare_dbs_parser.add_argument('--branch', default='master', help="git branch from which to download forms; THIS "
                                                                       "SHOULD NOT BE CHANGED BY REGULAR USERS")
    prepare_dbs_parser.add_argument('--keep_database_files', default=False, action='store_true',
                                    help="Keep unporcessed database files")
    prepare_dbs_parser.add_argument('--threads', default=10, type=int,
                                    help="Number of threads to use building mmseqs2 databases")
    prepare_dbs_parser.add_argument('--verbose', default=False, action='store_true', help="Make it talk more")
    prepare_dbs_parser.set_defaults(func=prepare_databases)

    # parser for setting database locations when you already have processed database files
    set_db_locs_parser.add_argument('--kegg_db_loc', default=None, help='mmseqs2 database file from kegg .pep file')
    set_db_locs_parser.add_argument('--uniref_db_loc', default=None, help='mmseqs2 database file from uniref .faa')
    set_db_locs_parser.add_argument('--pfam_db_loc', default=None, help='mmseqs2 database file from pfam .hmm')
    set_db_locs_parser.add_argument('--pfam_hmm_dat', default=None, help='pfam hmm .dat file to get PF descriptions')
    set_db_locs_parser.add_argument('--dbcan_db_loc', default=None,
                                    help='hmm file for dbcan, already processed with hmmpress')
    set_db_locs_parser.add_argument('--dbcan_fam_activities', default=None, help='CAZY family activities file')
    set_db_locs_parser.add_argument('--vogdb_db_loc', default=None,
                                    help='hmm file for vogdb, already processed with hmmpress')
    set_db_locs_parser.add_argument('--viral_db_loc', default=None,
                                    help='mmseqs2 database file from ref seq viral gene collection')
    set_db_locs_parser.add_argument('--peptidase_db_loc', default=None,
                                    help='mmseqs2 database file from MEROPS database')
    set_db_locs_parser.add_argument('--description_db_loc', default=None,
                                    help="Location to write description sqlite db")
    set_db_locs_parser.add_argument('--genome_summary_form_loc', default=None, help="File path to genome summary form")
    set_db_locs_parser.add_argument('--module_step_form_loc', default=None, help="File path to module step form")
    set_db_locs_parser.add_argument('--etc_module_database_loc', default=None, help="File path to etc module database")
    set_db_locs_parser.add_argument('--function_heatmap_form_loc', default=None,
                                    help="File path to function heatmap form")
    set_db_locs_parser.add_argument('--amg_database_loc', default=None, help="File path to amg database")
    set_db_locs_parser.add_argument('--update_description_db', action='store_true', default=False)
    set_db_locs_parser.set_defaults(func=set_database_paths)

    # parser for updating database descriptions
    update_description_db_parser.set_defaults(func=populate_description_db)

    # parser for printing out database configuration information
    print_db_locs_parser.set_defaults(func=print_database_locations)

    # parser for annotating vgfs
    annotate_parser.add_argument('-i', '--input_fasta', help="fasta file, output from ", required=True)
    annotate_parser.add_argument('-v', '--virsorter_affi_contigs', help="VirSorter VIRSorter_affi-contigs.tab "
                                                                             "output file", required=True)
    annotate_parser.add_argument('-o', '--output_dir', help="output directory")
    annotate_parser.add_argument('--min_contig_size', type=int, default=5000,
                                 help='minimum contig size to be used for gene prediction')
    annotate_parser.add_argument('--bit_score_threshold', type=int, default=60,
                                 help='minimum bitScore of search to retain hits')
    annotate_parser.add_argument('--rbh_bit_score_threshold', type=int, default=350,
                                 help='minimum bitScore of reverse best hits to retain hits')
    annotate_parser.add_argument('--custom_db_name', action='append', help="Names of custom databases, can be used"
                                                                                "multiple times.")
    annotate_parser.add_argument('--custom_fasta_loc', action='append',
                                 help="Location of fastas to annotated against, can be used multiple times but"
                                           "must match nubmer of custom_db_name's")
    annotate_parser.add_argument('--skip_uniref', action='store_true', default=False,
                                 help='Skip annotating with UniRef, drastically decreases run time and memory'
                                           'requirements')
    annotate_parser.add_argument('--skip_trnascan', action='store_true', default=False)
    annotate_parser.add_argument('--keep_tmp_dir', action='store_true', default=False)
    annotate_parser.add_argument('--threads', type=int, default=10, help='number of processors to use')
    annotate_parser.add_argument('--verbose', action='store_true', default=False)
    annotate_parser.set_defaults(func=annotate_vgfs)

    # parser for summarizing genomes
    distill_parser.add_argument("-i", "--input_file", help="Annotations path")
    distill_parser.add_argument("-o", "--output_dir", help="Directory to write summarized genomes")
    distill_parser.add_argument("--groupby_column", help="Column from annotations to group as VGF units",
                                default='scaffold')
    distill_parser.add_argument("--max_auxiliary_score", type=int, default=3,
                                help="Maximum auxiliary score to consider gene as potential AMG")
    distill_parser.add_argument("--remove_transposons", default=False, action='store_true',
                                help="Do not consider genes on scaffolds with transposons as potential AMGs")
    distill_parser.add_argument("--remove_fs", default=False, action='store_true',
                                help="Do not consider genes near ends of scaffolds as potential AMGs")
    distill_parser.set_defaults(func=summarize_vgfs)

    # parser for getting genes
    strainer_parser.add_argument('-i', '--input_annotations', required=True, help='annotations file to pull genes from')
    strainer_parser.add_argument('-f', '--input_fasta', required=True, help='fasta file to filter')
    strainer_parser.add_argument('-o', '--output_fasta', default='pull_genes.fasta',
                                 help='location to write filtered fasta')
    strainer_parser.add_argument('--fastas', nargs='*', default=None, help='space separated list of fastas to keep')
    strainer_parser.add_argument('--scaffolds', nargs='*', default=None,
                                 help='space separated list of scaffolds to keep')
    strainer_parser.add_argument('--genes', nargs='*', default=None, help='space separated list of genes to keep')
    strainer_parser.add_argument('--identifiers', nargs='*', default=None, help='database identifiers to keep')
    strainer_parser.set_defaults(func=pull_sequences)

    args = parser.parse_args()
    args_dict = {i: j for i, j in vars(args).items() if i != 'func'}
    args.func(**args_dict)