import pandas as pd

file_path = 'ECEGeneral_091823_SeniorDesign.xlsx'
output_file_path = 'output_file.csv'
grad_column = 'What is your expected graduation date from college? '

def change_month(date):
    if pd.notnull(date):
        month_mapping = {6: 5, 4: 5, 7: 8, 9: 8, 10: 12, 11: 12, 1: 5, 2: 5, 3: 5}
        return date.replace(month=month_mapping.get(date.month, date.month))
    return date

def format_season(date):
    if pd.notnull(date):
        season_map = {5: 'Spring', 8: 'Summer', 12: 'Fall'}
        season = season_map.get(date.month, '')
        return f' {date.year} {season}' if season else date.strftime('%Y')
    return date

df = pd.DataFrame(pd.read_excel(file_path))

df_filter = df[(df['Cumulative GPA'] >= 3.5)].copy()
df_filter[grad_column] = pd.to_datetime(df_filter[grad_column], format='%Y/%m/%d', errors='coerce')

df_complete = df_filter.sort_values(by = [grad_column, 'Cumulative GPA'], ascending=[True, False])
df_complete[grad_column] = df_complete[grad_column].apply(change_month)
df_complete[grad_column] = df_complete[grad_column].apply(format_season)

df_complete.to_csv(output_file_path, index=False)
