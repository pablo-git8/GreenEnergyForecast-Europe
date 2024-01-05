![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![terminal](https://img.shields.io/badge/windows%20terminal-4D4D4D?style=for-the-badge&logo=windows%20terminal&logoColor=white)
![git](https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white)
![markdown](https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white)
![powershell](https://img.shields.io/badge/powershell-5391FE?style=for-the-badge&logo=powershell&logoColor=white)
![jupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?style=for-the-badge&logo=Jupyter)

## GreenEnergyForecast-Europe: Schneider Hackathon Project

<p align="center">
	<img src="https://content.cdntwrk.com/files/aHViPTY1NzI0JmNtZD1pdGVtZWRpdG9yaW1hZ2UmZmlsZW5hbWU9aXRlbWVkaXRvcmltYWdlXzYwNzVhYTk3OGFmOTYuanBnJnZlcnNpb249MDAwMCZzaWc9YTliNWViYjRiODhhMTUxYzQ5Y2Y1NGM4YmRhMmI4Mzg%253D" alt="400" width="600"/>
</p>

### Project Overview
This project, developed for the Schneider Electric Hackathon, focuses on predicting the European country with the highest surplus of green energy in the next hour. The aim is to optimize the use of green energy, thereby reducing the carbon footprint of the computing industry. The project ranks in the top 20 at the European Schneider Hackathon.

### Context
With the increasing importance of sustainable computing, this project leverages data-driven insights to predict green energy surpluses across nine European countries, aiding in energy-efficient decision-making.

### Data Source
Data was obtained from the ENTSO-E Transparency portal (https://transparency.entsoe.eu/), providing time-series data of electricity consumption, wind, solar, and other green energy generation.

### Repo Structure
- **data/**: Contains raw and processed datasets.
- **docs/**: Project documentation and additional resources.
- **models/**: Serialized models and training weights.
- **notebooks/**: Jupyter notebooks for data analysis and model prototyping.
- **predictions/**: Outputs from the models.
- **reports/**: Analysis reports with figures and tables.
- **scripts/**: Utility scripts to run the project.
- **src/**: Source code for the project's main functionality.
- **requirements.txt**: Lists the project's Python dependencies.

### Key Features
- Data Processing: Data from the API was normalized to 1-hour intervals, focusing on green energy sources and consumption.
- Model: Utilized an ARIMA model to forecast the country with the highest green energy surplus.
- Automation: `run_pipeline.sh` for seamless data ingestion to model prediction.
- Evaluation: Model trained and validated using the created datasets.

### Installation and Usage
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. **Using Docker (Recommended)**
   - Build the Docker image: `docker build -t entsoe_pipeline_image .`
   - Run the Docker container, passing the necessary environment variables for API access:
     ```
     docker run -e ENTSOE_API_URL=https://web-api.tp.entsoe.eu/api -e ENTSOE_SECURITY_TOKEN=your_security_token entsoe_pipeline_image
     ```
     Replace `your_security_token` with your actual ENTSO-E Transparency portal security token.
4. **Without Docker**
   - Ensure `pipeline.conf` is configured with the correct API URL and security token.
   - Run `bash scripts/run_pipeline.sh` to execute the full pipeline. The script will automatically use the configuration from `pipeline.conf` if environment variables are not set.

### Contributions
This project is a result of collaborative efforts for the Schneider Electric Hackathon. Feel free to fork, modify, and use the project in compliance with the provided license.

### Acknowledgements
Special thanks to Schneider Electric and the ENTSO-E Transparency portal for providing the data and challenge platform.

### License
MIT
