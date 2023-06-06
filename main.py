import pandas as pd
import numpy as np
import streamlit as st
import datetime
import openpyxl

from func_collection import Graph
from func_collection import Func
import func_collection as fc

st.set_page_config(page_title='ハウス集計')
st.markdown('## ハウス催事集計')

@st.cache_data(ttl=datetime.timedelta(hours=1))
def make_data(file):
    df = pd.read_excel(
    file, sheet_name='見積照会', \
        usecols=[1, 3, 7, 8, 9, 10, 11, 15, 17, 10, 20, 22]) #index　ナンバー不要　index_col=0

    df['見積番号2'] = df['催事見積番号'].apply(lambda x: x[:8])
    df['品番'] = df['商品コード'].apply(lambda x: x.split()[0]) #品番
    df['張地'] = df['商　品　名'].apply(lambda x: x.split()[2] if len(x.split()) >= 4 else '')
    df['塗色'] = df['商品コード'].apply(lambda x: x.split()[1] if len(x.split()) >= 2 else '') #品番

    # ***INT型への変更***
    df[['数量', '販売金額', '金額']] = \
        df[['数量', '販売金額', '金額']].fillna(0).astype('int64')
    #fillna　０で空欄を埋める

    #分類
    #Dスツール/チェア用クッションはliving扱い
    cates = []
    for cate in df['商　品　名']:
        #living
        if 'ﾘﾋﾞﾝｸﾞﾃｰﾌﾞﾙ' in cate:
            cates.append('ltable') 
        elif 'ｻｲﾄﾞﾃｰﾌﾞﾙ' in cate:
            cates.append('stable')
        elif 'ｿﾌｧﾃｰﾌﾞﾙ' in cate:
            cates.append('stable')
        elif 'カウチ' in cate:
            cates.append('sofa')
        elif 'ｶｳﾁ' in cate:
            cates.append('sofa')
        elif 'ｿﾌｧ' in cate:
            cates.append('sofa')
        elif 'ﾎﾞﾙｽﾀｰ' in cate:
            cates.append('living')
        elif 'ｸｯｼｮﾝ' in cate:
            cates.append('living') 
        elif 'ｽﾂｰﾙ' in cate:
            cates.append('lstool') 
        elif 'AVｷｬﾋﾞﾈｯﾄ' in cate:
            cates.append('av')
        elif 'SHS' in cate:
            cates.append('shs')
        elif 'HCS' in cate:
            cates.append('hcs') 
        elif 'ｷｬﾋﾞﾈｯﾄ' in cate:
            cates.append('box') 
        elif 'ｼｪﾙﾌ' in cate:
            cates.append('box')
        #dining
        elif 'HTS' in cate:
            cates.append('dtable')
        elif 'HTZ' in cate:
            cates.append('dtable') 
        elif 'SNOT' in cate:
            cates.append('dtable')
        elif 'ﾃｰﾌﾞﾙ' in cate:
            cates.append('dtable')
        elif 'ﾁｪｱ' in cate:
            cates.append('chair')
        elif 'ﾍﾞﾝﾁ' in cate:
            cates.append('bench')
        #else
        else:
            cates.append('else')
    
    df['分類'] = cates

    #LD分類
    lds = []
    for cate in df['分類']:
        if cate in ['ltable', 'stable', 'sofa', 'living', 'lstool', 'av', 'shs', 'hcs', 'box']:
            lds.append('living')
        elif cate in ['dtable', 'chair', 'bench']:
            lds.append('dining')
        else:
            lds.append('else') 

    df['ld分類'] = lds 


    return df

# ***ファイルアップロード 今期***
uploaded_file = st.sidebar.file_uploader('ファイル', type='xlsx', key='now')
df = pd.DataFrame()
if uploaded_file:
    df = make_data(uploaded_file)


else:
    st.info('ファイルを選択してください。')
    st.stop()

custs = list(df['得意先名'].unique())
custs.insert(0, '全体')

selected_cust = st.sidebar.selectbox(
    '得意先名を選択',
    custs,
    key='scust'
)

df1 = pd.DataFrame()
if selected_cust == '全体':
    df1 = df
else:
    df1 = df[df['得意先名'] == selected_cust]

#インスタンス化
graph = Graph()
func = Func()

def overview():
    func.overview(df1, graph)
 
def category():
    func.category(df1, graph)

def series():
    func.series(df1, graph)
 
def hinban():
    func.hinban(df1, graph)

# def association_calc():
#     func.association(df1)


 





def main():
    # アプリケーション名と対応する関数のマッピング
    apps = {
        '-': None,
        '売上集計': overview,
        'アイテム別集計': category,
        'シリーズ別集計': series,
        '品番別集計': hinban,
        # 'アソシーエーション分析': association_calc,

          
    }
    selected_app_name = st.sidebar.selectbox(label='分析項目の選択',
                                             options=list(apps.keys()))                                     

    if selected_app_name == '-':
        st.info('サイドバーから分析項目を選択してください')
        st.stop()

    # 選択されたアプリケーションを処理する関数を呼び出す
    render_func = apps[selected_app_name]
    render_func()

if __name__ == '__main__':
    main()