import argparse
import os
import pandas as pd
import re
import json
from functools import reduce

def data_wrangling(input_file, output_file):
    # TODO: Save processed data to a CSV file

    directory = "../jupyter_notebook/data_samples"
    date_parser = lambda x: pd.to_datetime(x[:22])
    dataframes = []
    dict_of_dfs = {}
    energy_type_codes_to_filter = ['B01', 'B09', 'B10', 'B11', 'B12', 'B13', 'B15','B16', 'B18', 'B19']

    for filename in os.listdir(directory):
    
        match = re.match(r'gen_[A-Z]{2}_(\w{3})\.csv', filename)

        if match:
            energy_type = match.group(1)

            if energy_type in energy_type_codes_to_filter:
                
                df = pd.read_csv(os.path.join(directory, filename), converters={'EndTime': date_parser})

                _, country, energy_type = filename.split('_')
                energy_type = energy_type.replace('.csv', '') # Remove the file extension

                df['CountryCode'] = country
                df['EnergyTypeCode'] = energy_type
                
                df.dropna(inplace=True)

                df['EndTime'] = pd.to_datetime(df['EndTime'])

                df['TimeDifference'] = df['EndTime'].diff().dt.total_seconds() / 60

                sampling_period = int(df.loc[(df['TimeDifference'] > 0) & (df['TimeDifference'] <= 60), 'TimeDifference'].min())

                df.set_index('EndTime', inplace=True)
                
                sampling_period=str(sampling_period)
                df = df.resample(f'{sampling_period}T').asfreq()
                
                df['DateHour'] = df.index.floor('H')
                
                df.reset_index('EndTime', inplace=True)

                grouped_df = df.groupby('DateHour')['quantity'].sum().reset_index()
                
                grouped_df = grouped_df.rename(columns={'quantity': 'HourlySum'})

                df = pd.merge(df, grouped_df, how='left', left_on='DateHour', right_on='DateHour')
                
                df=df[~((df['quantity'].isnull())&(df['HourlySum']==0))]

                df.interpolate(method='linear', limit_direction='both', inplace=True)

                df.set_index('EndTime',inplace=True)

                numeric_cols = df.select_dtypes(include=['number'])
                categorical_cols = df.select_dtypes(exclude=['number', 'datetime64[ns]', 'bool'])

                resampled_df_num = numeric_cols.resample('H').sum()

                resampled_df_cat= categorical_cols.resample('H').last()

                resampled_df = pd.concat([resampled_df_num, resampled_df_cat], axis=1)

                resampled_df.dropna(inplace=True)

                dict_of_dfs[f'{country}_{energy_type}']=resampled_df


    dataframes_to_drop = ['SP_B10', 'SE_B13']

    for dataframe_name in dataframes_to_drop:
        dict_of_dfs.pop(dataframe_name, None)

    dic_gen = {}

    for name, df in dict_of_dfs.items():
        gen_key = name.split('_')[0]
        if gen_key not in dic_gen:
            dic_gen[gen_key] = {}  # Inicializa un diccionario vacío para esta clave si no existe
        df.rename(columns={'quantity':f'quantity_{name}'},inplace=True)
        dic_gen[gen_key][name] = df[[f'quantity_{name}']]

    dict_of_dfs_gen={}

    for name,df in dic_gen.items():
        dataframes_inner = list(dic_gen[name].values())
        result_inner = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True, how='inner'), dataframes_inner)
        
        result_inner['quantity_sum'] = result_inner.filter(like='quantity').sum(axis=1)
        
        dict_of_dfs_gen[name]=result_inner[['quantity_sum']]

    dict_of_dfs_load = {}

    for filename in os.listdir(directory):

        if re.match(r'load_[A-Z]{2}+\.csv', filename):
            
            df = pd.read_csv(os.path.join(directory, filename), converters={'EndTime': date_parser}).set_index('EndTime')
            
            _, country = filename.split('_')
            
            country = country.replace('.csv', '') # Remove the file extension
                    
            numeric_cols = df.select_dtypes(include=['number'])
            categorical_cols = df.select_dtypes(exclude=['number', 'datetime64[ns]', 'bool'])
            
            resampled_df_num = numeric_cols.resample('H').sum()

            resampled_df_cat= categorical_cols.resample('H').last()
            
            resampled_df = pd.concat([resampled_df_num, resampled_df_cat], axis=1)
            
            dict_of_dfs_load[country]=resampled_df[['Load']]

    generation=dict_of_dfs_gen.copy()
    load=dict_of_dfs_load.copy()

    final_dict={}
    for name in generation:
        result=pd.merge(generation[name],load[name],left_index=True,right_index=True,how='inner')
        final_dict[name]=result
    
    surplus_per_country={}
    for name in final_dict:
        final_dict[name]['surplus']=final_dict[name]['quantity_sum']-final_dict[name]['Load']

    concatenated_df = pd.concat(final_dict.values(), keys=final_dict.keys(), names=['country_code'])


    return concatenated_df
    


def parse_arguments():
    parser = argparse.ArgumentParser(description='Data processing script for Energy Forecasting Hackathon')
    parser.add_argument(
        '--input_file',
        type=str,
        default='data/raw_data.csv',
        help='Path to the raw data file to process'
    )
    parser.add_argument(
        '--output_file', 
        type=str, 
        default='data/processed_data.csv', 
        help='Path to save the processed data'
    )
    return parser.parse_args()

def main(input_file, output_file):
    #df = load_data(input_file)
    #df_clean = clean_data(df)
    #df_processed = preprocess_data(df_clean)
    data_wrangling(input_file, output_file)

if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_file, args.output_file)