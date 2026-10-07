# CFG449 fetch log (owner-approved for this lane, chat 10-07)

All fetches were made on 2026-10-07 between 11:08 and 11:20 UTC. Saved files carry a sha256. Probes not saved are marked "—". WebSearch summaries were used only to find URLs, never for numbers.

| URL | bytes | sha256 | stored at / note |
|---|---|---|---|
| https://cdsarc.cds.unistra.fr/ftp/J/AJ/162/80/ReadMe | 283 | — | HTTP 404: Anand+2021 is not on VizieR |
| https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-meta.all&-source=2021AJ....162...80A | — | — | empty result (no catalogue for this bibcode) |
| https://vizier.cds.unistra.fr/viz-bin/votable?-source=J/AJ/162*&-meta | — | — | J/AJ/162/80 absent |
| http://edd.ifa.hawaii.edu/ and http://edd.ifa.hawaii.edu/dfirst.php | 21471 / 224466 | — | table menu; kcmd = "CMDs/TRGB (Jacobs+2009; Anand+2021)", 558 entries |
| http://edd.ifa.hawaii.edu/dsecond.php (POST tblbool[]=kcmd, rows 1-5) | 3818 | a06eaab312c4a01e0af533b33404619645c8ff0276d7a9fdbd8fc66527eed905 | _external_data/cfg449/edd_dsecond_kcmd_probe.html: reCAPTCHA page, NOT bypassed |
| http://edd.ifa.hawaii.edu/describe_columns.php?table=kcmd | 11390 | — | column descriptions only |
| https://arxiv.org/e-print/2104.02649 (Anand+2021 source) | 79056106 | e07ef2622be7944947ab389c8006cc39657b41c99a4220b408fc2c3c2cd6b699 | _external_data/cfg449/anand21_arxiv_2104.02649.tar.gz: contains no data table |
| https://www.sao.ru/lv/lvgdb/tables.php (POST table=table6) | 14292 | — | returns the link ./tables/lvg_table6.dat (LVG last update 2026-07-13) |
| https://www.sao.ru/lv/lvgdb/tables/lvg_table6.dat | 94336 | ed1ee7245dc0cd58190df09385545e123d7af7d61962ad29532be0450891914a | data/lvg_table6.dat (LVG list of distances) |
| https://www.sao.ru/lv/lvgdb/tables/lvg_table1.dat | 204923 | 18df3f4c6115847e6510fe94508027f4916bb5543a1f8ca430540687eeadbee9 | data/lvg_table1.dat (LVG catalogue, positions) |
| https://arxiv.org/e-print/1611.03865 (Iorio+2017 source) | 8528077 | 5003a361318f89eb29ae4820a6f4e39079f5c85ac292ec2418ecc61dd81227cb | _external_data/cfg449/iorio17_arxiv_1611.03865.tar.gz: footnote points to the authors' site |
| http://www.filippofraternali.com/styled-9/index.html | 2204 | — | HTTP 404 (the old link in the paper) |
| https://www.filippofraternali.com/ and /downloads | 577758 / 443681 | — | the downloads page links "complete dataset of circular velocities for 17 LITTLE THINGS galaxies" (Iorio+2017) |
| https://www.dropbox.com/s/t4j8dacmnwgj0yb/finalrot.zip?dl=1 | 28572 | d4c456c65801f65742a6c5b2b377cbd7c05b30db1acca75523554d0b98ce2285 | data/iorio17_finalrot.zip (17 *_onlinetab.txt + ddo216b) |
| https://academic.oup.com/mnras/article/466/4/4159/2843767 | 5503 | — | HTTP 403 (MNRAS page not reachable) |
| https://export.arxiv.org/api/query (ti/abs/all "BIG-SPARC"; au:Haubner AND au:Lelli; Iorio; Anand) | — | — | metadata only: BIG-SPARC = arXiv 2411.13329 (IAU S392 proceedings), no data paper |
| https://astroweb.case.edu/SPARC/ | 7895 | — | no BIG-SPARC mention |
| https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-meta&-words=SPARC | — | — | only the 2016 SPARC catalogues; no BIG-SPARC |
