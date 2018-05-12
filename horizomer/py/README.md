### Python scripts used in this work

All scripts depend on Python 3.5+ with scikit-bio 0.5.1, unless otherwise stated.

#### Basic tree operations

**assign_node_ids.py**: Assign incremental node IDs to a tree in level order.

**remove_supports.py**: Remove node support values from a tree.

**root_by_outgroup.py**: Re-root a tree with a given set of taxa as the outgroup.

**order_nodes.py**: Re-order nodes of a tree in increasing or decreasing order.

#### Specialized tree operations

**order_nodes_centered.py**: Re-order nodes of tree in a way such that the two basal clades are in increasing and decreasing order, respectively. If the input tree is already midpoint-rooted, the output tree will shape like a triangle.

**root_by_outgroup_w_support.py**: Re-root a tree with a given set of taxa as the outgroup. This version can handle branch support values correctly.

#### Tool-specific utilities

**phylophlan_summarize.py**: Generate marker map and summarize genome to marker matches.
 - `/projects/genome_annotation/20170307/markers/phylophlan/scripts/phylophlan_summarize.py`

**phylophlan_extract.py**: Extract marker gene sequences based on PhyloPhlAn result.
 - `/projects/genome_annotation/20170307/markers/phylophlan/scripts/phylophlan_extract.py`

**phylosift_summarize.py**: Summarize the number of hits per marker per genome.
 - `/projects/genome_annotation/20170307/markers/phylosift/scripts/phylosift_summarize.py`

**phylosift_extract.py**: Extract marker gene sequences from search result.
 - `/projects/genome_annotation/20170307/markers/phylosift/scripts/phylosift_extract.py`

#### Taxonomy utilities

**shrink_taxdump.py**: Shrink the standard NCBI taxdump files `nodes.dmp` and `names.dmp` so that they only contain given TaxIDs and their ancestors
 - `/projects/genome_annotation/profiling/scripts/shrink_taxdump.py`

**taxdump_to_tree.py**: Build a tree based on NCBI taxdump.
 - `/projects/genome_annotation/20170307/taxonomy/scripts/taxdump_to_tree.py`

**tree_to_taxonomy.py**: Generate pseudo taxonomic hierarchies based on a tree.
 - `/projects/genome_annotation/profiling/scripts/tree_to_taxonomy.py`
 