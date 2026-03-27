import os
import pandas as pd



def combine_pages(
        pages_dir: str,
        batch_size: int = 100, 
        save_path: str = os.path.join('.', 'customs_data.csv')
):
    """Сборка json файлов в один csv файл

    Args:
        pages_dir (str): Путь с файлами результатами постраничной выгрузки с api
    """    
    file_name = os.listdir(pages_dir)[0]
    
    if not os.path.exists(save_path):
        # Инициализация итогового файла первым файлом
        file_name = os.listdir(pages_dir)[0]
        file_path = os.path.join(
            pages_dir,
            file_name,
        )
        df = pd.read_json(file_path)
        df.to_csv(save_path, index=False)
        os.remove(file_path)

    while True:
        df = pd.read_csv(save_path)

        file_names = os.listdir(pages_dir)[:batch_size]
        dfs = [pd.read_json(os.path.join(pages_dir, el)) for el in file_names]
        dfs.append(df)
        combined_df = pd.concat(dfs, ignore_index=True)
        combined_df.to_csv(save_path, index=False)
        _ = [os.remove(os.path.join(pages_dir, el)) for el in file_names]        

        if len(os.listdir(pages_dir)) == 0: break
