#!/usr/bin/env python3
"""
AlphaFold Job Generator: Top 10 Aromatic Clamps
==============================================

Selects the most promising evolved and designer peptides from today's
discovery and generates the AlphaFold Server JSON for submission.

SPDX-License-Identifier: AGPL-3.0-or-later
Copyright (C) 2026 Carl Zimmerman
"""

import json
import os

# Target sequences for AlphaFold
TARGET_SEQUENCES = {
    "KRAS_G12D": "MTEYKLVVVGADGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQVVIDGETCLLDILDTAGQEEYSAMRDQYMRTGEGFLCVFAINNTKSFEDIHHYREQIKRVKDSEDVPMVLVGNKCDLPSRTVDTKQAQDLARSYGIPFIETSAKTRQRVEDAFYTLVREIRQYRLKKISKEEKTPGCVKIKKCIIM",
    "p53_DNA_Binding": "MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPGPDEAPRMPEAAPPVAPAPAAPTPAAPAPAPSWPLSSSVPSQKTYQGSYGFRLGFLHSGTAKSVTCTYSPALNKMFCQLAKTCPVQLWVDSTPPPGTRVRAMAIYKQSQHMTEVVRRCPHHERCSDSDGLAPPQHLIRVEGNLRVEYLDDRNTFRHSVVVPYEPPEVGSDCTTIHYNYMCNSSCMGGMNRRPILTIITLEDSSGNLLGRNSFEVRVCACPGRDRRTEEENLRKKGEPHHELPPGSTKRALPNNTSSSPQPKKKPLDGEYFTLQIRGRERFEMFRELNEALELKDAQAGKEPGGSRAHSSHLKSKKGQSTSRHKKLMFKTEGPDSD",
    "BACE1": "MAQALPWLLLWMGAGVLPAHGTQHGIRLPLRSGLGGAPLGLRLPRETDEEPEEPGRRGSFVEMVDNLRGKSGQGYYVEMTVGSPPQTLNILVDTGSSNFAVGAAPHPFLHRYYQRQLSSTYRDLRKGVYVPYTQGKWEGELGTDLVSIPHGPNVTVRANIAAITESDKFFINGSNWEGILGLAYAEIARPDDSLEPFFDSLVKQTHVPNLFSLQLCGAGFPLNQSEVLASVGGSMIIGGIDHSLYTGSLWYTPIRREWYYEVIIVRVEINGQDLKMDCKEYNYDKSIVDSGTTNLRLPKKVFEAAVKSIKAASSTEKFPDGFWLGEQLVCWQAGTTPWNIFPVISLYLMGEVTNQSFRITILPQQYLRPVEDVATSQDDCYKFAISQSSTGTVMGAVIMEGFYVVFDRARKRIGFAVSACHVHDEFRTAAVEGPFVTLDMEDCGYNIPQTDESTLMTIAYVMAAICALFMLPLCLMVCQWCCLRCLRQQHDDFADDISLLK",
    "PCSK9": "MGTVASRRSRLLLVLLLLLLLLGPEPAAAGEDDEDGDYEELVLALRSEEDGLAEAPEHGTTATFHRCAKDPWRLPGTYVVVLKEETHLSQSERTARRLQAQAARRGYLTKILHVFHGLLPGFLVKMSGDLLELALKLPHVDYIEEDSSVFAQSIPWNLERITPPRYRADEYQPPDGGSLVEVYLLDTSIQSDHREIEGRVMVTDFENVPEEDGTRFHRQASKCDSHGTHLAGVVSGRDAGVAKGASMRSLRVLNCQGKGTVSGTLIGLEFIRKSQLVQPVGPLVVLLPLAGGYSRVLNAACQRLARAGVVLVTAAGNFRDDACLYSPASAPEVITVGATNAQDQPVTLGTLGTNFGRCVDLFAPGEDIIGASSDCSTCFVSQSGTSQAAAHVAGIAAMMLSAEPELTLAELRQRLIHFSAKDVINEAWFPEDQRVLTPNLVAALPPSTHGAGWQLFCRTVWSAHSGPTRMATAVARCAPDEELLSCSSFSRSGKRRGERMEAQGGKLVCRAHNAFGGEGVYAIARCCLLPQANCSVHTAPPAEASMGTRVHCHQQGHVLTGCSSHWEVEDLGTHKPPVLRPRGQPNQCVGHREASIHASCCHAPGLECKVKEHGIPAPQEQVTVACEEGWTLTGCSALPGTSHVLGAYAVDNTCVVRSRDVSTTGSTSEGAVTAVAICCRSRHLAQASQELQ",
}

def main():
    # Load evolved peptides
    evolved_path = '/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech/prior_art_factory/evolved_clamp_prior_art.json'
    if not os.path.exists(evolved_path):
        print("Error: evolved_clamp_prior_art.json not found.")
        return
        
    with open(evolved_path, 'r') as f:
        data = json.load(f)
    
    registry = data['registry']
    
    # Group by target for variety
    targets = {}
    for p in registry:
        t = p['target']
        if t not in targets: targets[t] = []
        targets[t].append(p)
    
    top_10 = []
    # Pick top 3 from BACE1, 3 from PCSK9, 2 from KRAS, 2 from p53
    # Sorted within each target by attractor hits
    for t_name in ["BACE1", "PCSK9", "KRAS_G12D", "p53_DNA_Binding"]:
        t_list = targets.get(t_name, [])
        t_list.sort(key=lambda x: (-x['target_attractor_hits'], -len(x['sequence'])))
        count_to_add = 3 if t_name in ["BACE1", "PCSK9"] else 2
        top_10.extend(t_list[:count_to_add])
    
    top_10 = top_10[:10] # Ensure exactly 10
    
    jobs = []
    for i, p in enumerate(top_10):
        target_name = p['target']
        target_seq = TARGET_SEQUENCES.get(target_name)
        
        if not target_seq:
            print(f"Warning: No sequence for {target_name}")
            continue
            
        # Determine symmetry (from earlier TARGETS dict knowledge)
        # BACE1 and PCSK9 are monomers in the active form for docking generally
        # KRAS is monomer. p53 DNA binding is often tetramer but monomer is fine for initial clamp screening.
        count = 1
        
        job = {
            "name": f"EVO_CLAMP_{i+1:02d}_{target_name}",
            "modelSeeds": [1],
            "sequences": [
                {
                    "protein": {
                        "sequence": target_seq
                    }
                },
                {
                    "protein": {
                        "sequence": p['sequence']
                    }
                }
            ]
        }
        jobs.append(job)
        print(f"Selected: {p['sequence']} for {target_name} (Hits: {p['target_attractor_hits']})")

    # Output to user-requested JSON
    out_path = '/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech/prior_art_factory/top_10_alphafold_jobs.json'
    with open(out_path, 'w') as f:
        json.dump(jobs, f, indent=2)
        
    print(f"\n✅ Top 10 AlphaFold jobs saved: {out_path}")

if __name__ == "__main__":
    main()
