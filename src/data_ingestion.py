import argparse
import pandas as pd
import configparser
import os
from utils import perform_get_request, xml_to_load_dataframe, xml_to_gen_data
from datetime import datetime, timedelta


def get_load_data_from_entsoe(regions, periodStart='202302240000', periodEnd='202303240000', output_path='./data'):
    
    # Try to get API details from environment variables first
    api_url = os.getenv('ENTSOE_API_URL')
    securityToken = os.getenv('ENTSOE_SECURITY_TOKEN')

    # If environment variables are not set, fall back to the pipeline.conf file
    if not api_url or not securityToken:
        parser = configparser.ConfigParser()
        parser.read("../pipeline.conf")
        api_url = parser.get("entsoe_api_config", "api_url")  # URL of the RESTful API
        securityToken = parser.get("entsoe_api_config", "securityToken")

    # Convert string dates to datetime objects
    start_date = datetime.strptime(periodStart, '%Y%m%d%H%M')
    end_date = datetime.strptime(periodEnd, '%Y%m%d%H%M')

    # Reading data in chunks
    while start_date < end_date:
        chunk_end_date = min(start_date + timedelta(days=365), end_date)
        chunk_start_str = start_date.strftime('%Y%m%d%H%M')
        chunk_end_str = chunk_end_date.strftime('%Y%m%d%H%M')

        # General parameters for the API
        # Refer to https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html#_documenttype
        params = {
            'securityToken': securityToken,
            'documentType': 'A65',
            'processType': 'A16',
            'outBiddingZone_Domain': 'FILL_IN', # used for Load data
            'periodStart': chunk_start_str, # in the format YYYYMMDDHHMM
            'periodEnd': chunk_end_str # in the format YYYYMMDDHHMM
        }

        # Loop through the regions and get data for each region
        for region, area_code in regions.items():

            print(f'Fetching data for {region}...')
            params['outBiddingZone_Domain'] = area_code
        
            # Use the requests library to get data from the API for the specified time range
            response_content = perform_get_request(api_url, params)

            # Response content is a string of XML data
            df = xml_to_load_dataframe(response_content)
            # Save the DataFrame to a CSV file
            df.to_csv(f'{output_path}/load_{region}.csv', index=False)
        
        # Update start_date for next iteration
        start_date = chunk_end_date

    return


def get_gen_data_from_entsoe(regions, periodStart='202302240000', periodEnd='202303240000', output_path='./data'):
    
    # Try to get API details from environment variables first
    api_url = os.getenv('ENTSOE_API_URL')
    securityToken = os.getenv('ENTSOE_SECURITY_TOKEN')

    # If environment variables are not set, fall back to the pipeline.conf file
    if not api_url or not securityToken:
        parser = configparser.ConfigParser()
        parser.read("../pipeline.conf")
        api_url = parser.get("entsoe_api_config", "api_url")  # URL of the RESTful API
        securityToken = parser.get("entsoe_api_config", "securityToken")

    # Convert string dates to datetime objects
    start_date = datetime.strptime(periodStart, '%Y%m%d%H%M')
    end_date = datetime.strptime(periodEnd, '%Y%m%d%H%M')
    
    # Reading data in chunks
    while start_date < end_date:
        chunk_end_date = min(start_date + timedelta(days=1), end_date)
        chunk_start_str = start_date.strftime('%Y%m%d%H%M')
        chunk_end_str = chunk_end_date.strftime('%Y%m%d%H%M')

        # General parameters for the API
        params = {
            'securityToken': securityToken,
            'documentType': 'A75',
            'processType': 'A16',
            'outBiddingZone_Domain': 'FILL_IN', # used for Load data
            'in_Domain': 'FILL_IN', # used for Generation data
            'periodStart': chunk_start_str, # in the format YYYYMMDDHHMM
            'periodEnd': chunk_end_str # in the format YYYYMMDDHHMM
        }

        # Loop through the regions and get data for each region
        for region, area_code in regions.items():
            print(f'Fetching data for {region}...')
            params['outBiddingZone_Domain'] = area_code
            params['in_Domain'] = area_code
        
            # Use the requests library to get data from the API for the specified time range
            response_content = perform_get_request(api_url, params)

            # Response content is a string of XML data
            dfs = xml_to_gen_data(response_content)

            # Save the dfs to CSV files
            for psr_type, df in dfs.items():
                # Save the DataFrame to a CSV file
                df.to_csv(f'{output_path}/gen_{region}_{psr_type}.csv', index=False)
        
        # Update start_date for next iteration
        start_date = chunk_end_date
    
    return


def parse_arguments():
    parser = argparse.ArgumentParser(description='Data ingestion script for Energy Forecasting')
    parser.add_argument(
        '--start_time', 
        type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), 
        default=datetime.datetime(2023, 1, 1), 
        help='Start time for the data to download, format: YYYY-MM-DD'
    )
    parser.add_argument(
        '--end_time', 
        type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), 
        default=datetime.datetime(2023, 1, 2), 
        help='End time for the data to download, format: YYYY-MM-DD'
    )
    parser.add_argument(
        '--output_path', 
        type=str, 
        default='./data',
        help='Name of the output file'
    )
    return parser.parse_args()


def main(start_time, end_time, output_path):
    
    regions = {
        'HU': '10YHU-MAVIR----U',
        'IT': '10YIT-GRTN-----B',
        'PO': '10YPL-AREA-----S',
        'SP': '10YES-REE------0',
        'UK': '10Y1001A1001A92E',
        'DE': '10Y1001A1001A83F',
        'DK': '10Y1001A1001A65H',
        'SE': '10YSE-1--------K',
        'NE': '10YNL----------L',
    }

    # Transform start_time and end_time to the format required by the API: YYYYMMDDHHMM
    start_time = start_time.strftime('%Y%m%d%H%M')
    end_time = end_time.strftime('%Y%m%d%H%M')

    # Get Load data from ENTSO-E
    get_load_data_from_entsoe(regions, start_time, end_time, output_path)

    # Get Generation data from ENTSO-E
    get_gen_data_from_entsoe(regions, start_time, end_time, output_path)


if __name__ == "__main__":
    args = parse_arguments()
    main(args.start_time, args.end_time, args.output_path)