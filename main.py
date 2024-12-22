import flet as ft
from pathlib import Path
import pandas as pd
import pdb
import shutil
import subprocess
import io
import pretty_errors
import time
#----------------------------------------------------------------------

PRIMARY_COLOR=ft.colors.TEAL_ACCENT_700
SECOND_COLOR=ft.colors.AMBER
THIRD_COLOR=ft.colors.PINK_500

VOCABULARY_ORIGINAL_FILE = './assets/V/VERBEN'
VOCABULARY_FILE = './assets/v1.csv'
#======================================================================
class TrainingApp(ft.Column):
    def __init__(self, card_data: pd.DataFrame):
        super().__init__()
        self.card_data = card_data
        self.card_data_index = 0

        self.card_table = ft.DataTable()
        self.card_table_view = ft.Container()

        # read card_data to ft.DataTable 
        self.set_card_table()

        #----------------------------------------------------------------------
        # buttons

        self.save_button = ft.ElevatedButton(
                content = ft.Container(
                    content = ft.Text(
                        "Save", 
                        size = 18
                    ), 
                ),
                bgcolor=PRIMARY_COLOR,
                color=SECOND_COLOR,
                on_click=self.save_rf
        )

        #--------------------------
        self.sort_az_button = ft.ElevatedButton(
                content = ft.Container(
                    content = ft.Text(
                        "A-Z", 
                        size = 18
                    ), 
                ),
                bgcolor=SECOND_COLOR,
                color=PRIMARY_COLOR,
                on_click=self.sort_card_data_az,
        )

        self.sort_f_button = ft.ElevatedButton(
                content = ft.Container(
                    content = ft.Text(
                        "Fehler", 
                        size = 18
                    ), 
                ),
                bgcolor=SECOND_COLOR,
                color=PRIMARY_COLOR,
                on_click=self.sort_card_data_f,
        )

        self.sort_stamm_button = ft.ElevatedButton(
                content = ft.Container(
                    content = ft.Text(
                        "Stamm", 
                        size = 18
                    ), 
                ),
                bgcolor=SECOND_COLOR,
                color=PRIMARY_COLOR,
                on_click=self.sort_card_data_stamm,
        )
        self.shuffle_button = ft.ElevatedButton(
                content = ft.Container(
                    content = ft.Text(
                        "Shuffle", 
                        size = 18
                    ), 
                ),
                bgcolor=SECOND_COLOR,
                color=PRIMARY_COLOR,
                on_click=self.sort_card_data_shuffle,
        )
        #----------------------------------------------------------------------
        self.buttons = ft.Container(
            content = ft.Row([
                        self.sort_az_button, 
                        self.sort_f_button, 
                        self.sort_stamm_button, 
                        self.shuffle_button, 

                        ], 
                        alignment = ft.MainAxisAlignment.CENTER,
        ) 
        )

        self.buttons_view = ft.Container(
            content = ft.Column([self.buttons]
            ), 
            margin = ft.margin.only(top=64),
            alignment=ft.alignment.center
        )

        #----------------------------------------------------------------------
        filter_buttons_list = ['A','B','E','G','I','M','R','T','W']

        self.filter_buttons = [
                ft.ElevatedButton(
                content = ft.Container(
                    content = ft.Text(
                        x,
                        size = 20
                    ), 
                    padding = 0,
                ),
                color=SECOND_COLOR,
                bgcolor=PRIMARY_COLOR,
                on_click=self.filter_card_data,
                )

                for x in filter_buttons_list
              ] 

        self.filters = ft.Container(
            content = ft.Row(
                self.filter_buttons,
                alignment = ft.MainAxisAlignment.CENTER,
            ) 
        )

        self.filter_view = ft.Container(
            content = ft.Column([self.filters]
            ), 

            alignment=ft.alignment.center
        )

        #----------------------------------------------------------------------


        #----------------------------------------------------------------------
        self.controls = [self.buttons_view,
                         self.filter_view,
                         self.card_table_view]

    #----------------------------------------------------------------------
    def filter_card_data(self, e) -> None:

        x = e.control.content.content.value


        self.card_data = self.card_data.sort_values(by='Q', ignore_index=True)
        self.card_data_index = self.card_data.loc[self.card_data['Q'] > x.lower()].index[0]
      

        self.set_card_table()
        self.controls = [self.buttons_view,
                        self.filter_view,
                        self.card_table_view]

        self.update()
    #----------------------------------------------------------------------
    def set_card_table(self) -> None:

        self.card_table = ft.DataTable(
            columns = self.headers(self.card_data) ,
            rows = self.rows(self.card_data.iloc[self.card_data_index:]),

            column_spacing = 12,

            data_row_max_height = 40,
            )

        self.card_table_view = ft.Container(
            content = ft.Column(
                controls = [self.card_table],
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,

            ), 

            alignment=ft.alignment.center
        )

    #----------------------------------------------------------------------
    def sort_card_data_az(self, e) -> None:
        self.card_data_index = 0

        self.card_data = self.card_data.sort_values(by='Q',

        )


        self.card_data.reindex()
        self.set_card_table()

        self.controls = [self.buttons_view,
                        self.filter_view,
                        self.card_table_view]

        self.update()

    #----------------------------------------------------------------------
    def sort_card_data_f(self, e) -> None:
        self.card_data_index = 0

        self.card_data = self.card_data.sort_values(by='F', 
                                                    ascending=False,

        )


        self.set_card_table()
        self.controls = [self.buttons_view,
                         self.filter_view,
                         self.card_table_view]
        self.update()

    #----------------------------------------------------------------------
    def sort_card_data_stamm(self, e) -> None:
        self.card_data_index = 0


        self.card_data['stamm'] = self.card_data['Q'].map(lambda x: x[::-1])

        self.card_data = self.card_data.sort_values(by='stamm',)
        self.card_data = self.card_data.drop(['stamm'], axis=1)


        self.set_card_table()

        self.controls = [self.buttons_view,
                        self.filter_view,
                        self.card_table_view]
        self.update()

    #----------------------------------------------------------------------
    def sort_card_data_shuffle(self, e) -> None:
        self.card_data_index = 0

        self.card_data = self.card_data.sample(n=len(self.card_data))
        self.card_data.reindex()




        self.set_card_table()
        self.controls = [self.buttons_view,
                        self.filter_view,
                        self.card_table_view]
        self.update()

    #----------------------------------------------------------------------
    def save_rf(self, e) -> None:

# change only the row in question


        backup_file = VOCABULARY_FILE+".update"
        shutil.copy(VOCABULARY_FILE, backup_file)


        self.card_data.to_csv(VOCABULARY_FILE, index=False)

    #----

    def read_whole_datatable(self, e) -> pd.DataFrame:
        card_data = []
        card_columns = ['Q', 'A', 'R', 'F']

        for r in self.card_table.rows:

            y = [x.content.value for x in r.cells]            
            y.remove('しっとる')
            y.remove('しらん')

            card_data.append(y)

        df = pd.DataFrame(card_data, 
                        columns = card_columns, 

        )
        df['R'] = df['R'].astype(int)
        df['F'] = df['F'].astype(int)

        return df

    #----------------------------------------------------------------------
    # ft.DataTable

    def headers(self, df : pd.DataFrame) -> list:

         return [ft.DataColumn(ft.Text('')),
                 ft.DataColumn(ft.Text('')),
                 ft.DataColumn(ft.Text('')),
                 ft.DataColumn(ft.Text('')),
                 ft.DataColumn(ft.Text('R')),
                 ft.DataColumn(ft.Text('F')),

         ]

    def rows(self, df : pd.DataFrame) -> list:
        rows = []

        positive_button = ft.DataCell(ft.Text("しっとる"), on_tap=self.show_answer)
        negative_button = ft.DataCell(ft.Text("しらん"), on_tap=self.show_answer)

        for index, row in df.iterrows():
            rows.append(ft.DataRow(
                cells = [

                        ft.DataCell(
                        content=ft.Text(row['Q'],
                        font_family='Open Sans',
                        size=18), 
                        ), 
                        ft.DataCell(ft.Text(row['A'], color=THIRD_COLOR, opacity=0.0)),
                        
                        ft.DataCell(ft.Text("しっとる", 
                                    color=SECOND_COLOR, 
                                    ),
                                    on_tap=self.show_answer
                        ),
                        ft.DataCell(ft.Text("しらん", 
                                    color=PRIMARY_COLOR, 
                                    ),
                                    on_tap=self.repeat_question
                        ),



                        ft.DataCell(ft.Text(row['R'])),
                        ft.DataCell(ft.Text(row['F'])),
                        ft.DataCell(ft.Text(row['hash']), 
                                    visible=False),
                ]
                ))
        return rows

    #----------------------------------------------------------------------
    def repeat_question(self, e):


# get hash
        hash_data_table = (e.control.parent.cells[6].content.value)


# find the row in card_data

        # make answer visible
        e.control.parent.cells[1].content.opacity=1.0        

        # update repetition    
        r = (int(e.control.parent.cells[4].content.value))
        r += 1
        e.control.parent.cells[4].content.value = str(r)


        self.card_data.loc[self.card_data['hash'] == hash_data_table, ['R']] = r

        # update failure

        f = (int(e.control.parent.cells[5].content.value))
        f += 1
        e.control.parent.cells[5].content.value = str(f)

        self.card_data.loc[self.card_data['hash'] == hash_data_table, ['F']] = f



        # update display
        self.update()

        time.sleep(2.0) 

        e.control.parent.cells[1].content.opacity=0.0        

        self.save_rf(e)
        self.update()

    #----------------------------------------------------------------------
    def show_answer(self, e):

        hash_data_table = (e.control.parent.cells[6].content.value)


        e.control.parent.cells[1].content.opacity=1.0        

        # update repetition    
        r = (int(e.control.parent.cells[4].content.value))
        r += 1
        e.control.parent.cells[4].content.value = str(r)


        self.card_data.loc[self.card_data['hash'] == hash_data_table, ['R']] = r


        self.save_rf(e)
        self.update()


#======================================================================
# Quick stationary
#----------------------------------------------------------------------
def load_card_data(file_path):

    #------------  

    proc = subprocess.Popen(["sh", "conv1.sh", 
                            file_path],
                            stdout = subprocess.PIPE)


    output, error =  proc.communicate()

    with io.StringIO(output.decode()) as b:
        df_original = pd.read_csv(b,
            dtype={'Q': object, 'A': object, 'R': 'Int64', 'F': 'Int64'},
            comment="#", 
            header=0,
            on_bad_lines='warn',

        )

    df_original = df_original.drop_duplicates(subset=['A', 'Q'])

    # create hash column
    df_original['hash'] = pd.util.hash_pandas_object(df_original[['Q', 'A']], 
                                                     categorize = True, 
                                                     index=False)

    #------------  
    # read from datatable an store it => skip. do it with 'Save'.

    #------------  
    # back up working vocabulary file 
    backup_file = VOCABULARY_FILE+".bak"
    shutil.copy(VOCABULARY_FILE, backup_file)

    df_current = pd.read_csv(Path(VOCABULARY_FILE),
        dtype={'Q': object, 'A': object, 'R': 'Int64', 'F': 'Int64'},
                                comment="#", 
                                header=0,
                                on_bad_lines='warn',
    )

    df_current = df_current.drop_duplicates(subset=['A', 'Q'])
    # create hash column
    df_current['hash'] = pd.util.hash_pandas_object(df_current[['Q', 'A']],
                                                     categorize = True, 
                                                     index=False)


    df = df_original.merge(df_current, on=['hash'], how='left', 
            suffixes=['', '_'], 
    )

    df = df[['Q', 'A', 'R_', 'F_', 'hash']].fillna(0)
    df = df.rename(columns = {'R_': 'R', 'F_': 'F'})

    return df
#======================================================================
def main(page: ft.Page):


    page.fonts = {

        "Open Sans": "fonts/OpenSans-VariableFont_wdth,wght.ttf",
        "IBMPlexSansJP": "fonts/IBMPlexSansJP-SemiBold.ttf",
    }

    page.theme_mode = "light"    
    page.scroll = "adaptive"
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(primary=PRIMARY_COLOR,
                                    secondary=SECOND_COLOR),
        font_family="IBMPlexSansJP",
    )

    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER


    card_data = load_card_data(Path(VOCABULARY_ORIGINAL_FILE))    
    page.update()
    app = TrainingApp(card_data)

    page.add(app)


ft.app(main)
#======================================================================
# END
#======================================================================
