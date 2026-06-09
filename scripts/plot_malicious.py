#!/usr/bin/env python3
import pathlib
import pandas as pd
import plotly.express as px

# Define the MAC mapping for pruning as used in dataset.py
MAC_MAPPING = {
    "WebOS_binary.csv": "18:56:80:17:d0:ef",
    "Server_Binary.csv": "a4:bb:6d:ac:e1:fd",
    "Raspberry_Webmine_Robust.csv": "dc:a6:32:67:66:4b",
    "Raspberry_Binary.csv": "dc:a6:32:68:35:8a",
    "Raspberry_Webmine_Aggressive.csv": "dc:a6:32:67:66:4b",
    "Raspberry_WebminePool_Aggressive.csv": "dc:a6:32:67:66:4b",
    "Server_WebminePool_Aggressive.csv": "a4:bb:6d:ac:e1:fd",
    "Server_WebminePool_Robust.csv": "a4:bb:6d:ac:e1:fd",
    "Raspberry_WebminePool_Stealthy.csv": "dc:a6:32:67:66:4b",
    "Raspberry_WebminePool_Robust.csv": "dc:a6:32:68:35:8a",
    "Desktop_WebminePool_Aggressive.csv": "d8:3b:bf:8f:ba:ba",
}

def parse_filename(filename):
    base = filename.replace(".csv", "")
    parts = base.split("_")
    
    device = parts[0]
    
    if len(parts) == 2:
        attack_raw = parts[1]
        strategy = "None"
    elif len(parts) == 3:
        attack_raw = parts[1]
        strategy = parts[2]
    else:
        attack_raw = parts[1]
        strategy = "_".join(parts[2:])
        
    attack_raw_lower = attack_raw.lower()
    if "webminepool" in attack_raw_lower:
        attack_type = "Webminepool"
    elif "webmine" in attack_raw_lower:
        attack_type = "webmine"
    elif "binary" in attack_raw_lower:
        attack_type = "binary"
    else:
        attack_type = attack_raw
        
    return device, attack_type, strategy

def main():
    malicious_dir = pathlib.Path("Data/malicious")
    data_rows = []
    
    for file_path in sorted(malicious_dir.glob("*.csv")):
        filename = file_path.name
        device, attack_type, strategy = parse_filename(filename)
        
        df = pd.read_csv(file_path)
        
        # Apply pruning filter (MAC address match)
        mac = MAC_MAPPING.get(filename)
        if mac:
            df_pruned = df[(df["HW_dst"] == mac) | (df["Hw_src"] == mac)]
            n_rows = len(df_pruned)
        else:
            n_rows = len(df)
            
        data_rows.append({
            "device": device,
            "attack_type": attack_type,
            "strategy": strategy,
            "n_rows": n_rows,
            "filename": filename
        })
        print(f"Processed {filename}: device={device}, attack_type={attack_type}, strategy={strategy}, n_rows={n_rows}")
        
    df_summary = pd.DataFrame(data_rows)
    summary_csv_path = pathlib.Path("data/malicious_summary.csv")
    summary_csv_path.parent.mkdir(parents=True, exist_ok=True)
    df_summary.to_csv(summary_csv_path, index=False)
    print(f"\nSaved summary CSV to {summary_csv_path}")
    print(df_summary)
    
    # Generate the bar chart
    fig = px.bar(
        df_summary,
        x="device",
        y="n_rows",
        color="attack_type",
        title="Distribuição de Pacotes Maliciosos por Dispositivo e Tipo de Ataque",
        labels={"device": "Dispositivo", "n_rows": "Número de Pacotes (Linhas)", "attack_type": "Tipo de Ataque"},
        barmode="group",
        template="plotly_white"
    )
    
    # Save the plot
    plot_img_path = pathlib.Path("report/imagens/malicious_distribution.png")
    plot_img_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_image(str(plot_img_path), width=800, height=500, scale=2)
    print(f"Saved plot image to {plot_img_path}")

if __name__ == "__main__":
    main()
