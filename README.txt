=================================================================================================================================
			      NASARI: a Novel Approach for a Semantically-Aware Representation of Items

				  José Camacho Collados, Mohammad Taher Pilehvar and Roberto Navigli
=================================================================================================================================


This package contains vector representations for BabelNet Synsets and Wikipedia pages in several languages.

=================================================================================================================================
FORMAT OF THE VECTORS REPRESENTATIONS
=================================================================================================================================

Each line in the vectors correspond to a BabelNet synset (its id appears in the first column). In the cases where the BabelNet 
synset is associated with a Wikipedia page, the Wikipedia page title is also specified, underscore separated (e.g. United_States). 
If no Wikipedia page is associated with a given BabelNet synset, it is written -NA- instead. 


We release three types of vectors:

1. [Lexical vectors] the dimensions correspond to lemmas (including multiword expressions).

	Files: NASARI_lexical_*.txt 

	Format (TAB separated): 
		BabelSynsetId  WikipediaPageTitle  lemma1_weight1  lemma2_weight2 ...
		

2. [Unified vectors] the dimensions correspond to the BabelNet synsets (represented by their IDs).

	Files: NASARI_unified_*.txt

	Format (TAB separated): 
		BabelSynsetId  WikipediaPageTitle  synset1_weight1  synset2_weight2 ...


Please note that the dimensions of lexical and unified vectors are separated from the weights using an underscore. 
Also note that the vectors are truncated to the non-zero dimensions only and sorted according to the weights of their dimensions.

3. [Embed vectors] are embedded vector representations of 300 dimensions (the first line indicates the number of synsets and the 
dimensions):

	Files: NASARI_embed_*.txt 

	Format (SPACE separated): 
		BabelSynsetId__WikipediaPageTitle  dimension1  dimension2 ... dimension300
		
		(Note that the separator between BabelSynsetId and WikipediaPageTitle is a DOUBLE underscore)

=================================================================================================================================
INSTRUCTIONS FOR CALCULATING SEMANTIC SIMILARITY
=================================================================================================================================

  - The unified vectors have Babel Synsets as their dimensions and hence are comparable across languages. 

  - We recommend Weighted Overlap for computing the similarity between our lexical and unified vectors, 
    and cosine for the embedded vectors.  

  - For more information on our vectors please read the following papers.


=================================================================================================================================
REFERENCE PAPER
=================================================================================================================================

When using these resources, please refer to one of the following papers:

	José Camacho-Collados, Mohammad Taher Pilehvar and Roberto Navigli. 
	A Unified Multilingual Semantic Representation of Concepts.
	In Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics (ACL 2015), 
	Beijing, China, July 27-29, 2015, pp. 741-751.
	
	José Camacho-Collados, Mohammad Taher Pilehvar and Roberto Navigli. 
	NASARI: a Novel Approach to a Semantically-Aware Representation of Items. 
	In Proceedings of the North American Chapter of the Association for Computational Linguistics (NAACL 2015), 
	Denver, USA, May-June, 2015, pp. 567-577.

=================================================================================================================================
CONTACT
=================================================================================================================================
 
If you have any enquiries about any of the resources, please contact José Camacho Collados (collados [at] di.uniroma1 [dot] it),
Mohammad Taher Pilehvar (pilehvar [at] di.uniroma1 [dot] it) and Roberto Navigli (navigli [at] di.uniroma1 [dot] it).

=================================================================================================================================

NASARI is licensed under a Creative Commons Attribution-Noncommercial-Share Alike 3.0 License. For commercial inquiries, please 
contact us.


