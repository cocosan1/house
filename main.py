import pandas as pd
import streamlit as st
import datetime
import openpyxl

from func_collection import Graph

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

st.write(df)

st.write(df['品番'][1])
test = df['品番'][1]
num = test[2]
st.write(len(test))

#インスタンス化
graph = Graph()

def overview():
    sum_baika = df['販売金額'].sum()
    sum_gedai = df['金額'].sum()

    st.markdown('#### 売上集計/全体')
    graph.make_bar([sum_baika, sum_gedai], ['販売価格', '下代'])


    s_baika = df.groupby('得意先名')['販売金額'].sum()
    s_gedai = df.groupby('得意先名')['金額'].sum()

    #ソート
    s_baika.sort_values(inplace=True)
    s_gedai.sort_values(inplace=True)

    #売上集計
    st.markdown('##### 売上集計/得意先別')
    graph.make_bar_h_nonline(s_baika, s_baika.index, 'name?', '販売金額', 500)
    graph.make_bar_h_nonline(s_gedai, s_gedai.index, 'name?', '下代', 500)

    #構成比
    st.markdown('##### 構成比/下代')
    graph.make_pie(s_gedai, s_gedai.index)

def category():

    #下代
    sum_l = df[df['ld分類']=='living']['金額'].sum()
    sum_d = df[df['ld分類']=='dining']['金額'].sum()
    sum_e = df[df['ld分類']=='else']['金額'].sum()

    st.markdown('#### LD別集計')
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('##### LD別下代')
        graph.make_bar([sum_l, sum_d, sum_e], ['living', 'dining', 'else'])
    with col2:
        st.markdown('##### LD構成比')
        graph.make_pie([sum_l, sum_d, sum_e], ['living', 'dining', 'else'])
    
    #アイテム別集計
    df_l = df[df['ld分類']=='living']
    s_litem_cnt = df_l.groupby('分類')['数量'].sum()
    s_litem_sum = df_l.groupby('分類')['金額'].sum()

    s_litem_cnt.sort_values(ascending=False, inplace=True)
    s_litem_sum.sort_values(ascending=False, inplace=True)
    
    #数量
    st.markdown('#### ■ 数量')
    #living
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('##### リビング/アイテム別')
        graph.make_bar(s_litem_cnt[1:], s_litem_cnt.index[1:]) #その他抜く
    with col2:
        st.markdown('##### リビング/アイテム構成比')
        graph.make_pie(s_litem_cnt[1:], s_litem_cnt.index[1:])
    
    #dining
    df_d = df[df['ld分類']=='dining']
    s_ditem_cnt = df_d.groupby('分類')['数量'].sum()
    s_ditem_sum = df_d.groupby('分類')['金額'].sum()

    s_ditem_cnt.sort_values(ascending=False, inplace=True)
    s_ditem_sum.sort_values(ascending=False, inplace=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('##### ダイニング/アイテム別')
        graph.make_bar(s_ditem_cnt, s_ditem_cnt.index)
    with col2:
        st.markdown('##### ダイニング/アイテム構成比')
        graph.make_pie(s_ditem_cnt, s_ditem_cnt.index)
    
    #下代
    st.markdown('#### ■ 下代')
    #living
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('##### リビング/アイテム別')
        graph.make_bar(s_litem_sum, s_litem_sum.index)
    with col2:
        st.markdown('##### リビング/アイテム構成比')
        graph.make_pie(s_litem_sum, s_litem_sum.index)
    
    #dining
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('##### ダイニング/アイテム別')
        graph.make_bar(s_ditem_sum, s_ditem_sum.index)
    with col2:
        st.markdown('##### ダイニング/アイテム構成比')
        graph.make_pie(s_ditem_sum, s_ditem_sum.index)
    
    #アイテム別塗色
    #sofa
    df_sofa = df_l[df_l['分類']=='sofa']
    s_sofa = df_sofa.groupby('塗色')['数量'].sum()
    s_sofa.sort_values(ascending=False, inplace=True)

    st.markdown('#### 塗色別集計/数量')
    st.markdown('##### ■ ソファ')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('##### 数量')
        graph.make_bar(s_sofa, s_sofa.index)
    with col2:
        st.markdown('##### 構成比')
        graph.make_pie(s_sofa, s_sofa.index)
    
    #dtable
    df_dtable = df_d[df_d['分類']=='dtable']
    s_dtable = df_dtable.groupby('塗色')['数量'].sum()
    s_dtable.sort_values(ascending=False, inplace=True)

    st.markdown('##### ■ ダイニングテーブル')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('##### 数量')
        graph.make_bar(s_dtable, s_dtable.index)
    with col2:
        st.markdown('##### 構成比')
        graph.make_pie(s_dtable, s_dtable.index)
    
    #chair
    df_chair = df_d[df_d['分類']=='chair']
    s_chair = df_chair.groupby('塗色')['数量'].sum()
    s_chair.sort_values(ascending=False, inplace=True)

    st.markdown('##### ■ ダイニングチェア')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('##### 数量')
        graph.make_bar(s_chair, s_chair.index)
    with col2:
        st.markdown('##### 構成比')
        graph.make_pie(s_chair, s_chair.index)
    
    #アイテム別張地
    #sofa
    s_sofa2 = df_sofa.groupby('張地')['数量'].sum()
    s_sofa2.sort_values(ascending=False, inplace=True)

    st.markdown('#### 張地別集計/数量')
    st.markdown('##### ■ ソファ')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('##### 数量')
        graph.make_bar(s_sofa2, s_sofa2.index)
    with col2:
        st.markdown('##### 構成比')
        graph.make_pie(s_sofa2, s_sofa2.index)
    
    #chair
    s_chair2 = df_chair.groupby('張地')['数量'].sum()
    s_chair2.sort_values(ascending=False, inplace=True)

    st.markdown('##### ■ ダイニングチェア')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('##### 数量')
        graph.make_bar(s_chair2[1:], s_chair2.index[1:]) #板座外す
    with col2:
        st.markdown('##### 構成比')
        graph.make_pie(s_chair2[1:], s_chair2.index[1:])
    
    #塗色+張地
    #sofa
    s_sofa2 = df_sofa.groupby(['塗色', '張地'], as_index=False)['数量'].sum()
    # s_sofa2.sort_values(ascending=False, inplace=True)

    # st.markdown('#### 張地別集計/数量')
    # st.markdown('##### ■ ソファ')
    # col1, col2 = st.columns(2)
    # with col1:
    #     st.markdown('##### 数量')
    #     graph.make_bar(s_sofa2, s_sofa2.index)
    # with col2:
    #     st.markdown('##### 構成比')
    #     graph.make_pie(s_sofa2, s_sofa2.index)
    
    # #chair
    # s_chair2 = df_chair.groupby('張地')['数量'].sum()
    # s_chair2.sort_values(ascending=False, inplace=True)

    # st.markdown('##### ■ ダイニングチェア')
    # col1, col2 = st.columns(2)
    # with col1:
    #     st.markdown('##### 数量')
    #     graph.make_bar(s_chair2[1:], s_chair2.index[1:]) #板座外す
    # with col2:
    #     st.markdown('##### 構成比')
    #     graph.make_pie(s_chair2[1:], s_chair2.index[1:])


def series():
    st.markdown('#### シリーズ別下代')
    #下代
    df_l = df[df['ld分類']=='living']
    df_d = df[df['ld分類']=='dining']

    s_l = df_l.groupby('シリーズ名')['金額'].sum()
    s_d = df_d.groupby('シリーズ名')['金額'].sum()

    s_l.sort_values(ascending=False, inplace=True)
    s_d.sort_values(ascending=False, inplace=True)

    st.markdown('##### ■ リビング')
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('##### 下代')
        graph.make_bar(s_l, s_l.index)
    with col2:
        st.markdown('##### 構成比')
        graph.make_pie(s_l, s_l.index)
    
    st.markdown('##### ■ ダイニング')
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('##### 下代')
        graph.make_bar(s_d, s_d.index)
    with col2:
        st.markdown('##### 構成比')
        graph.make_pie(s_d, s_d.index)

    


def hinban():
    selected_cate = st.selectbox(
        '商品分類を選択',
        ['sofa', 'chair', 'dtable'],
        key='sc'
    )
    df_selected = df[df['分類']==selected_cate]


    s_cnt = df_selected.groupby('品番')['数量'].sum()
    s_sum = df_selected.groupby('品番')['金額'].sum()

    s_cnt.sort_values(ascending=False, inplace=True)
    s_sum.sort_values(ascending=False, inplace=True)

    st.markdown('#### ■ 品番別集計')

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('##### 品番別数量')
        graph.make_bar(s_cnt, s_cnt.index)
    with col2:
        st.markdown('##### 品番別構成比')
        graph.make_pie(s_cnt, s_cnt.index)






def main():
    # アプリケーション名と対応する関数のマッピング
    apps = {
        '-': None,
        '全体/売上集計': overview,
        '全体/アイテム別集計': category,
        '全体/シリーズ別集計': series,
        '全体/品番別集計': hinban,

          
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