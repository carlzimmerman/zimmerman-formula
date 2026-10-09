# CFG523 FETCH_LOG (public ALMA Science Archive; owner approval in chat 2026-10-09; budget 20 GB)

Work dir (outside git): `../../../_external_data/cfg523_work/`. Per-request records (label, URL, byte offset, bytes, sha256 of the bytes, UTC) are in `../../../_external_data/cfg523_work/FETCH_MANIFEST.jsonl`; the cumulative ledger is `../../../_external_data/cfg523_work/LEDGER.json`. All products are PUBLIC pipeline (`*.cube.I.pbcor.fits`) cubes; DataLink reported link_auth = false for every file used. Nothing proprietary or login-gated was requested.

**Total bytes received: 5,601,940,456 (5.602 GB) in 2423 requests**, including one 2026-10-09 range-support probe (223,694,848 bytes of the head of `member.uid___A001_X3788_X5cda.zC_406690_sci.spw15.cube.I.pbcor.fits`, sha256 9e684fd08f1fb64f403d6fec97f83efea2507d0c3193b94d9f34267146c9d101, deleted after the test).

## Metadata (TAP / DataLink)
| date | what | file | sha256 |
|---|---|---|---|
| 2026-10-09 | ALMA TAP sync ivoa.obscore, INTERSECTS(s_region, CIRCLE) per parent field group, s_resolution <= 0.6" | `../../../_external_data/cfg523_work/alma_rows_parents.csv` (10,877,653 B) | be6f4cb3ad0384acd4442be7c308a6f6c599ba5d6fc9adf63ea4fd3840715438 |
| 2026-10-09 | ALMA TAP sync ivoa.obscore, blind sweep S (see cfg523_sweep_results.json for the ADQL) | `../../../_external_data/cfg523_work/alma_rows_sweep.csv` (6,031,679 B) | 3b25b9949ceabd471dc210230d39a8d201509835e3f21d3e0fae6aef0e972b26 |
| 2026-10-09 | DataLink file list for MOUS A001_X144_Xef (astroquery.alma get_data_info) | `../../../_external_data/cfg523_work/datalink_A001_X144_Xef.ecsv` | d3b62b85eceb0805ee323191da41778585a6255ab7895638d2adce29a3c0ac2e |
| 2026-10-09 | DataLink file list for MOUS A001_X1465_X210e (astroquery.alma get_data_info) | `../../../_external_data/cfg523_work/datalink_A001_X1465_X210e.ecsv` | e9268dbed714e13eb7ebbc9ceb15b2cea9cd84f0691e98c3a2cca35ce7ca9309 |
| 2026-10-09 | DataLink file list for MOUS A001_X1465_X2112 (astroquery.alma get_data_info) | `../../../_external_data/cfg523_work/datalink_A001_X1465_X2112.ecsv` | 158d1dfa4dc38aede7235d5a9b493f7020e944bb6c3b0d8b313db54e39eae6d1 |
| 2026-10-09 | DataLink file list for MOUS A001_X1465_X35ca (astroquery.alma get_data_info) | `../../../_external_data/cfg523_work/datalink_A001_X1465_X35ca.ecsv` | 11f2f140abc74506741f304d865ab4e2d20f4e4795dd6bb0cc2c9cd4f5abeeb6 |
| 2026-10-09 | DataLink file list for MOUS A001_X2d1f_X68 (astroquery.alma get_data_info) | `../../../_external_data/cfg523_work/datalink_A001_X2d1f_X68.ecsv` | 0b63cfa0d87e94ed84bec3d6959a66b7cd6ca52fd18bc55042828e6d52e35c9d |
| 2026-10-09 | DataLink file list for MOUS A001_X2d1f_X74 (astroquery.alma get_data_info) | `../../../_external_data/cfg523_work/datalink_A001_X2d1f_X74.ecsv` | 92b28542869dbe44ebaca579c9d0e87af2e04fe5f3edf04aa27744a19f0aa469 |
| 2026-10-09 | DataLink file list for MOUS A001_X2fe_Xb0e (astroquery.alma get_data_info) | `../../../_external_data/cfg523_work/datalink_A001_X2fe_Xb0e.ecsv` | 9b47a38b4946219b2c39df9cd7abc2661bd404785f3ea92ce6939bbf4e546971 |
| 2026-10-09 | DataLink file list for MOUS A001_X2fe_Xb16 (astroquery.alma get_data_info) | `../../../_external_data/cfg523_work/datalink_A001_X2fe_Xb16.ecsv` | f760fbbcec213d0abf60c1ef04bb45607594f17144c6d8ed1101cae1efd8620d |
| 2026-10-09 | DataLink file list for MOUS A001_X3621_X1088 (astroquery.alma get_data_info) | `../../../_external_data/cfg523_work/datalink_A001_X3621_X1088.ecsv` | 80a165f843473c6d358070fe3a28a27ec6be0b519ddd658abf9b7528b12aa347 |
| 2026-10-09 | DataLink file list for MOUS A001_X362b_Xc71 (astroquery.alma get_data_info) | `../../../_external_data/cfg523_work/datalink_A001_X362b_Xc71.ecsv` | 19f8e6a60a59193c5d431580b56313bc9b617bf58226cf8bbcd3adb027ce5875 |
| 2026-10-09 | DataLink file list for MOUS A001_X3788_X5cda (astroquery.alma get_data_info) | `../../../_external_data/cfg523_work/datalink_A001_X3788_X5cda.ecsv` | b259e6cb81fc7b42f2cb9911229a4373b1859696546fbc1921efdb0f8f0973c8 |
| 2026-10-09 | DataLink file list for MOUS A002_X5a9a13_X7e0 (astroquery.alma get_data_info) | `../../../_external_data/cfg523_work/datalink_A002_X5a9a13_X7e0.ecsv` | 08913c863cf1ab2e819cc14219f11b42d61f6e091f235b5d4da0df788d90cff1 |

## Product byte ranges (headers and line sub-cubes)
| target | file (archive URL basename) | kind | requests | bytes | UTC first..last | sha256 over the per-request sha256 list |
|---|---|---|---|---|---|---|
| COS4_02672 | `member.uid___A001_X2d1f_X68.K3D_COS4_02672_sci.spw23.cube.I.pbcor.fits` | hdr | 24 | 276,480 | 2026-10-09T13:47:13Z..16:21:09Z | d2085eee953118e69dcb02e450f6dd9a… |
| COS4_02672 | `member.uid___A001_X2d1f_X68.K3D_COS4_02672_sci.spw25.cube.I.pbcor.fits` | hdr | 22 | 253,440 | 2026-10-09T13:47:38Z..16:21:36Z | 64c4ad2d24ecabccd8856642a24175bb… |
| COS4_02672 | `member.uid___A001_X2d1f_X68.K3D_COS4_02672_sci.spw27.cube.I.pbcor.fits` | hdr | 21 | 241,920 | 2026-10-09T13:48:42Z..16:22:00Z | 444b8f1526cc61894a6b4c5ea8884ea0… |
| COS4_02672 | `member.uid___A001_X2d1f_X68.K3D_COS4_02672_sci.spw29.cube.I.pbcor.fits` | hdr | 21 | 241,920 | 2026-10-09T13:49:08Z..16:22:22Z | ab960733698a6e93641d947c0081b356… |
| COS4_03324 | `member.uid___A001_X2d1f_X74.MOSDEF_3324_sci.spw25.cube.I.pbcor.fits` | hdr | 21 | 241,920 | 2026-10-09T13:49:31Z..16:22:49Z | 726a400a2a940cac765c224c41ebd04e… |
| COS4_03324 | `member.uid___A001_X2d1f_X74.MOSDEF_3324_sci.spw27.cube.I.pbcor.fits` | hdr | 21 | 241,920 | 2026-10-09T13:49:57Z..16:23:12Z | eae815e6b94990b5a3cb70d3c56f9a09… |
| COS4_03324 | `member.uid___A001_X2d1f_X74.MOSDEF_3324_sci.spw29.cube.I.pbcor.fits` | hdr | 21 | 241,920 | 2026-10-09T13:50:22Z..16:23:38Z | 7aa31d1701a25435a1d5cee450f74319… |
| COS4_03324 | `member.uid___A001_X2d1f_X74.MOSDEF_3324_sci.spw31.cube.I.pbcor.fits` | hdr | 21 | 241,920 | 2026-10-09T13:50:50Z..16:24:03Z | db1d9a21717b578ef01ddeb3504ef9ed… |
| COS4_19753 | `member.uid___A001_X362b_Xc71.COS_19753_sci.spw25.cube.I.pbcor.fits` | hdr | 21 | 241,920 | 2026-10-09T13:51:13Z..16:24:26Z | 618e055d34f6025e9ab336f8e0e1788e… |
| COS4_19753 | `member.uid___A001_X362b_Xc71.COS_19753_sci.spw27.cube.I.pbcor.fits` | hdr | 21 | 241,920 | 2026-10-09T13:51:40Z..16:24:52Z | 61c8f7b1b06bbdfbf8fe155a0e4b7087… |
| COS4_19753 | `member.uid___A001_X362b_Xc71.COS_19753_sci.spw29.cube.I.pbcor.fits` | hdr | 21 | 241,920 | 2026-10-09T13:52:02Z..16:25:15Z | f2e013c04e87957da7e562b6fc957d0e… |
| COS4_19753 | `member.uid___A001_X362b_Xc71.COS_19753_sci.spw31.cube.I.pbcor.fits` | hdr | 21 | 241,920 | 2026-10-09T13:52:29Z..16:25:41Z | 77f1edd623134dcb38b9ae73225336c5… |
| GS4_20422 | `member.uid___A001_X2fe_Xb16.HUDF-JVLA-ALMA_sci.spw17.cube.I.pbcor.fits` | hdr | 7 | 80,640 | 2026-10-09T13:52:53Z..16:25:47Z | d420e068ac532d9bf581f194ce9dbf1a… |
| GS4_20422 | `member.uid___A001_X2fe_Xb16.HUDF-JVLA-ALMA_sci.spw19.cube.I.pbcor.fits` | hdr | 7 | 80,640 | 2026-10-09T13:53:02Z..16:25:56Z | a77d4509a158d5d89e022a6976528ef6… |
| GS4_20422 | `member.uid___A001_X2fe_Xb16.HUDF-JVLA-ALMA_sci.spw21.cube.I.pbcor.fits` | hdr | 7 | 80,640 | 2026-10-09T13:53:10Z..16:26:06Z | 904ee1f15604632ec37dd8a079a14409… |
| GS4_20623 | `member.uid___A001_X3621_X1088.GS10578_XID746_sci.spw21.cube.I.pbcor.fits` | hdr | 21 | 241,920 | 2026-10-09T13:53:16Z..16:26:29Z | b31ed67e9c2cc1678d16a83b726ed0fb… |
| GS4_20623 | `member.uid___A001_X3621_X1088.GS10578_XID746_sci.spw23.cube.I.pbcor.fits` | hdr | 21 | 241,920 | 2026-10-09T13:53:43Z..16:26:55Z | ab241a6ade2a26e7ffda51c24f0b7748… |
| GS4_20623 | `member.uid___A001_X3621_X1088.GS10578_XID746_sci.spw25.cube.I.pbcor.fits` | hdr | 21 | 241,920 | 2026-10-09T13:54:06Z..16:27:18Z | 811ac7656abaf4fc40ff208b5537c6d3… |
| GS4_20623 | `member.uid___A001_X3621_X1088.GS10578_XID746_sci.spw9.cube.I.pbcor.fits` | hdr | 21 | 241,920 | 2026-10-09T13:54:33Z..16:27:44Z | 60bfbad6cdeecfbc410ce305d20a56cc… |
| GS4_35951 | `member.uid___A001_X2fe_Xb0e.HUDF-JVLA-ALMA_sci.spw17.cube.I.pbcor.fits` | hdr | 7 | 80,640 | 2026-10-09T13:54:57Z..16:27:50Z | a4b56026badd3357a0b4df9b2962d1ea… |
| COS4_05758 | `member.uid___A001_X1465_X35ca.DSFGJ100030_sci.spw17.cube.I.pbcor.fits` | hdr | 3 | 34,560 | 2026-10-09T13:55:06Z..13:55:20Z | ecb9479adc9bb81c7e396e14f5c00660… |
| ZC406690 | `member.uid___A001_X3788_X5cda.zC_406690_sci.spw15.cube.I.pbcor.fits` | hdr | 21 | 241,920 | 2026-10-09T13:55:28Z..16:28:40Z | 5b3f2275ac005f821650fd9ab9ecd18d… |
| ZC406690 | `member.uid___A001_X3788_X5cda.zC_406690_sci.spw19.cube.I.pbcor.fits` | hdr | 21 | 241,920 | 2026-10-09T13:55:55Z..16:29:06Z | be5fcfe9b57f63e66c6c27098bb15232… |
| ZC406690 | `member.uid___A001_X3788_X5cda.zC_406690_sci.spw21.cube.I.pbcor.fits` | hdr | 21 | 241,920 | 2026-10-09T13:56:20Z..16:29:31Z | 740a2649002bbc22f4f79be54b5503c4… |
| ZC406690 | `member.uid___A001_X3788_X5cda.zC_406690_sci.spw23.cube.I.pbcor.fits` | hdr | 3 | 34,560 | 2026-10-09T13:56:42Z..13:57:00Z | e91d49f392c9fce709d1059b5aa95eb0… |
| COS4_02672 | `member.uid___A001_X2d1f_X68.K3D_COS4_02672_sci.spw29.cube.I.pbcor.fits` | data | 181 | 390,960,000 | 2026-10-09T13:59:23Z..14:06:00Z | a6a86a3c865222752cb99e81d3625531… |
| COS4_03324 | `member.uid___A001_X2d1f_X74.MOSDEF_3324_sci.spw31.cube.I.pbcor.fits` | data | 181 | 246,044,160 | 2026-10-09T14:07:46Z..14:14:57Z | 23f4e517b8fe2b334ce4653162d19ffd… |
| COS4_19753 | `member.uid___A001_X362b_Xc71.COS_19753_sci.spw31.cube.I.pbcor.fits` | data | 173 | 291,470,400 | 2026-10-09T14:16:25Z..14:22:04Z | b3f809defdfe68ae144cd4bc7b0c7afa… |
| GS4_20422 | `member.uid___A001_X2fe_Xb16.HUDF-JVLA-ALMA_sci.spw21.cube.I.pbcor.fits` | data | 14 | 314,697,600 | 2026-10-09T14:22:39Z..14:23:09Z | 7b65f4f91c53dee5fa8d0ec3776307eb… |
| GS4_20623 | `member.uid___A001_X3621_X1088.GS10578_XID746_sci.spw9.cube.I.pbcor.fits` | data | 43 | 69,474,240 | 2026-10-09T14:24:56Z..14:26:19Z | 359a1bf900cc4706792b6923fd2628e7… |
| GS4_35951 | `member.uid___A001_X2fe_Xb0e.HUDF-JVLA-ALMA_sci.spw17.cube.I.pbcor.fits` | data | 104 | 2,337,753,600 | 2026-10-09T14:26:38Z..14:30:58Z | 6fa81d071a8097954e9889f9b53d3bce… |
| COS4_05758/COS4_05803 | `member.uid___A001_X1465_X35ca.DSFGJ100030_sci.spw17.cube.I.pbcor.fits` | hdr | 18 | 207,360 | 2026-10-09T14:31:10Z..16:28:17Z | ac29361d60aa1a9ac3d058f627bbdc83… |
| COS4_05758/COS4_05803 | `member.uid___A001_X1465_X35ca.DSFGJ100030_sci.spw17.cube.I.pbcor.fits` | data | 49 | 78,792,000 | 2026-10-09T14:31:33Z..14:33:09Z | 281a10efcd63adc0b6693d1e3a8ca6d1… |
| ZC406690 | `member.uid___A001_X3788_X5cda.zC_406690_sci.spw21.cube.I.pbcor.fits` | data | 231 | 413,538,048 | 2026-10-09T14:34:18Z..14:41:30Z | 8b2b20b0104ff02d2c689d861be90309… |
| ZC400569/ZC400569N | `member.uid___A001_X1465_X2112.zC-400569_sci.spw19.cube.I.pbcor.fits` | hdr | 3 | 34,560 | 2026-10-09T15:26:39Z..15:58:41Z | bcf91b45ce36a56366147a9808a84f06… |
| ZC400569/ZC400569N | `member.uid___A001_X1465_X2112.zC-400569_sci.spw23.cube.I.pbcor.fits` | hdr | 3 | 34,560 | 2026-10-09T15:26:45Z..15:58:47Z | cb70ec07a82dcd92f663d3b88542bb39… |
| ZC400569/ZC400569N | `member.uid___A001_X1465_X2112.zC-400569_sci.spw27.cube.I.pbcor.fits` | hdr | 3 | 34,560 | 2026-10-09T15:26:53Z..15:58:55Z | cc87236d73f134acf8a96ea6bf3cce3d… |
| ZC400569 | `member.uid___A001_X1465_X2112.zC-400569_sci.spw19.cube.I.pbcor.fits` | hdr | 1 | 11,520 | 2026-10-09T15:27:13Z..15:27:13Z | 90e32763dc20ef193aea8db5262dbcac… |
| ZC400569 | `member.uid___A001_X1465_X2112.zC-400569_sci.spw23.cube.I.pbcor.fits` | hdr | 1 | 11,520 | 2026-10-09T15:27:19Z..15:27:19Z | 44b403b47bdf7d0c3900a3364015e468… |
| ZC400569 | `member.uid___A001_X1465_X2112.zC-400569_sci.spw27.cube.I.pbcor.fits` | hdr | 1 | 11,520 | 2026-10-09T15:27:27Z..15:27:27Z | 4b9431b5e759bd0bd0ef95cc9b1b3f58… |
| ZC400569/ZC400569N | `member.uid___A001_X1465_X210e.zC-400569_sci.spw19.cube.I.pbcor.fits` | hdr | 2 | 23,040 | 2026-10-09T15:28:05Z..15:59:05Z | ac115b705726000bce51d8b4858097ef… |
| ZC400569/ZC400569N | `member.uid___A001_X1465_X210e.zC-400569_sci.spw25.cube.I.pbcor.fits` | hdr | 2 | 23,040 | 2026-10-09T15:28:11Z..15:59:14Z | 4c97bd70017f19a4d4d5ade495e7db4a… |
| ZC400569/ZC400569N | `member.uid___A001_X1465_X210e.zC-400569_sci.spw27.cube.I.pbcor.fits` | hdr | 2 | 23,040 | 2026-10-09T15:28:17Z..15:59:22Z | 3f1ff75eb0039d7463a6378554377e94… |
| ZC400569/ZC400569N | `member.uid___A001_X1465_X210e.zC-400569_sci.spw27.cube.I.pbcor.fits` | data | 973 | 1,230,066,600 | 2026-10-09T15:28:24Z..15:57:48Z | 796db1c92d74293a5f007a3b7e94c9fb… |

## Saved sub-cubes (cropped FITS written locally from the byte ranges above)
| file | bytes | sha256 |
|---|---|---|
| `../../../_external_data/cfg523_work/subcubes/member.uid___A001_X1465_X210e.zC-400569_sci.spw27.cube.I.pbcor.sub_CO4-3.fits` | 179,913,600 | f8d58b0dd4e6c87249b325a555244e78f487f458ff67807fe10ca4af29422868 |
| `../../../_external_data/cfg523_work/subcubes/member.uid___A001_X1465_X35ca.DSFGJ100030_sci.spw17.cube.I.pbcor.sub_CO3-2.fits` | 7,925,760 | e2dd2077399fbfb48916c4824781cb54e5ddc3d7ba7de4370b9591395fca3f2d |
| `../../../_external_data/cfg523_work/subcubes/member.uid___A001_X2d1f_X68.K3D_COS4_02672_sci.spw29.cube.I.pbcor.sub_CO3-2.fits` | 36,659,520 | f314f1f3ac2df3a421eeeac6349ab0a6d085c0fcadeb71d89f03675d8c2a482f |
| `../../../_external_data/cfg523_work/subcubes/member.uid___A001_X2d1f_X74.MOSDEF_3324_sci.spw31.cube.I.pbcor.sub_CO3-2.fits` | 22,688,640 | 678717ae8a457ae55f112c9176f3bf575ffcd322dc53a4dd7ec5973674d0a7e1 |
| `../../../_external_data/cfg523_work/subcubes/member.uid___A001_X2fe_Xb0e.HUDF-JVLA-ALMA_sci.spw17.cube.I.pbcor.sub_CI2-1.fits` | 186,192,000 | 7e88afa0837a3f8250c49978dc0213873f811f9b881de27d329ba7849bb2bb54 |
| `../../../_external_data/cfg523_work/subcubes/member.uid___A001_X2fe_Xb16.HUDF-JVLA-ALMA_sci.spw21.cube.I.pbcor.sub_CO7-6.fits` | 25,070,400 | 4206def69a8fab3cf651530b332ce150281982fc32ef907062c851c995945f20 |
| `../../../_external_data/cfg523_work/subcubes/member.uid___A001_X3621_X1088.GS10578_XID746_sci.spw9.cube.I.pbcor.sub_CO3-2.fits` | 6,022,080 | ec50ffafaa3b5f3b9b43ea07a2bfa16acf27edc168d25b7c502a4291452f5f2b |
| `../../../_external_data/cfg523_work/subcubes/member.uid___A001_X362b_Xc71.COS_19753_sci.spw31.cube.I.pbcor.sub_CO3-2.fits` | 26,320,320 | cea9591f5aadc2837c15cc2fbfa164a36dcc29db43b84986dfb6ce04679d95d6 |
| `../../../_external_data/cfg523_work/subcubes/member.uid___A001_X3788_X5cda.zC_406690_sci.spw21.cube.I.pbcor.sub_CO4-3.fits` | 61,989,120 | bbf56d0c0489d6c8d6d795478a0191c87d3b33b4e074cd25a056e07d6ad42874 |
