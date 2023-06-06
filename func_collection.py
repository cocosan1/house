import streamlit as st
import numpy as np
import plotly.graph_objects as go

from mlxtend.frequent_patterns import apriori #頻出アイテム集合を抽出する関数
from mlxtend.frequent_patterns import association_rules

class Graph():
        def make_bar(self, val_list, x_list):
            #可視化
            #グラフを描くときの土台となるオブジェクト
            fig = go.Figure()
            #今期のグラフの追加
            for (val, x) in zip(val_list, x_list):
                fig.add_trace(
                    go.Bar(
                        x=[x],
                        y=[val],
                        text=[round(val/10000) if int(val) >= 10000 else int(val)],
                        textposition="outside", 
                        name=x)
                )
            #レイアウト設定     
            fig.update_layout(
                showlegend=False #凡例表示
            )
            #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
            st.plotly_chart(fig, use_container_width=True) 

        #**********************************************************棒グラフ　今期前期
        def make_bar_nowlast(self, lists_now, lists_last, x_list):
            #可視化
            #グラフを描くときの土台となるオブジェクト
            fig = go.Figure()
            #今期のグラフの追加
            
            for (val_list, name) in zip([lists_now, lists_last], ['今期', '前期']) :
                fig.add_trace(
                    go.Bar(
                        x=x_list,
                        y=val_list,  
                        text=[round(val/10000) if val >= 10000 else int(val) for val in val_list],
                        textposition="outside", 
                        name=name)
                )
            #レイアウト設定     
            fig.update_layout(
                showlegend=True #凡例表示
            )
            #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
            st.plotly_chart(fig, use_container_width=True) 

        #**********************************************************棒グラフ　今期前期 小数
        def make_bar_nowlast_float(self, lists_now, lists_last, x_list):
            #可視化
            #グラフを描くときの土台となるオブジェクト
            fig = go.Figure()
            #今期のグラフの追加
            
            for (val_list, name) in zip([lists_now, lists_last], ['今期', '前期']) :
                fig.add_trace(
                    go.Bar(
                        x=x_list,
                        y=val_list,  
                        text=[round(val, 2) for val in val_list],
                        textposition="outside", 
                        name=name)
                )
            #レイアウト設定     
            fig.update_layout(
                showlegend=True #凡例表示
            )
            #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
            st.plotly_chart(fig, use_container_width=True) 
        
        #*************************************************************棒グラフ　横 基準線あり
         #可視化
        def make_bar_h(self, val_list, label_list, name, title, line_val, height):
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=val_list,
                y=label_list,
                marker_color='#87cefa',
                textfont={'color': '#696969'},
                name=name)
                )
            fig.update_traces(
                textposition='outside',
                texttemplate='%{x:0.2f}',
                orientation='h'
                )
            # 基準線の追加
            fig.add_shape(
                type="line",
                x0=line_val,  # 基準線の開始位置 (x座標)
                x1=line_val,  # 基準線の終了位置 (x座標)
                y0=label_list[0],  # 基準線の開始位置 (y座標)
                y1=label_list[-1],  # 基準線の終了位置 (y座標)
                line=dict(
                    color="red",
                    width=2,
                    dash="dash"  # 破線を使用する場合は "dash" を指定
        )
    )
            fig.update_layout(
                title=title,
                width=500,
                height=height,
                plot_bgcolor='white'
                )
            #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
            st.plotly_chart(fig, use_container_width=True) 
        
        #*************************************************************棒グラフ　横　基準線なし
         #可視化
        def make_bar_h_nonline(self, val_list, label_list, name, title, height):
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=val_list,
                y=label_list,
                marker_color='#87cefa',
                textfont={'color': '#696969'},
                name=name)
                )
            fig.update_traces(
                textposition='outside',
                texttemplate='%{x:.0f}',
                orientation='h'
                )

            fig.update_layout(
                title=title,
                width=500,
                height=height,
                plot_bgcolor='white'
                )
            #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
            st.plotly_chart(fig, use_container_width=True) 

        #**********************************************************折れ線
        def make_line(self, df_list, name_list, x_list):

            #グラフを描くときの土台となるオブジェクト
            fig = go.Figure()
            #今期のグラフの追加

            for (df, name) in zip(df_list, name_list):

                fig.add_trace(
                go.Scatter(
                    x=x_list, #strにしないと順番が崩れる
                    y=df,
                    mode = 'lines+markers+text', #値表示
                    text=[round(val/10000) if val >= 10000 else int(val) for val in df],
                    textposition="top center", 
                    name=name)
                    )  

            #レイアウト設定     
            fig.update_layout(
                showlegend=True #凡例表示
            )
            #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
            st.plotly_chart(fig, use_container_width=True) 
        
        #**********************************************折れ線　non_xlist    
        def make_line_nonXlist(self, df_list, name_list):
            #グラフを描くときの土台となるオブジェクト
            fig = go.Figure()
            #今期のグラフの追加

            for (df, name) in zip(df_list, name_list):

                fig.add_trace(
                go.Scatter(
                    x=['10月', '11月', '12月', '1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月'], #strにしないと順番が崩れる
                    y=df,
                    mode = 'lines+markers+text', #値表示
                    text=[round(val/10000) if val >= 10000 else int(val) for val in df],
                    textposition="top center", 
                    name=name)
                    )  

            #レイアウト設定     
            fig.update_layout(
                showlegend=True #凡例表示
            )
            #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅
            st.plotly_chart(fig, use_container_width=True) 
            
        #***************************************************************円
        def make_pie(self, vals, labels):

            # st.write(f'{option_category} 構成比(今期)')
            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=labels,
                        values=vals
                        )])
            fig.update_layout(
                showlegend=True, #凡例表示
                height=290,
                margin={'l': 20, 'r': 60, 't': 0, 'b': 0},
                )
            fig.update_traces(textposition='inside', textinfo='label+percent') 
            #inside グラフ上にテキスト表示
            st.plotly_chart(fig, use_container_width=True) 
            #plotly_chart plotlyを使ってグラグ描画　グラフの幅が列の幅

#***************************************************************************************func
class Func():
    def overview(self, df, graph):
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

    def category(self, df, graph):

        #下代
        sum_l = df[df['ld分類']=='living']['金額'].sum()
        sum_d = df[df['ld分類']=='dining']['金額'].sum()
        sum_e = df[df['ld分類']=='else']['金額'].sum()

        st.markdown('#### LD別集計')
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('##### 下代')
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
        df_chair2 = df_chair.copy()
        # 空白文字を NaN 値に置き換える
        df_chair2['張地'] = df_chair2['張地'].replace('', np.nan)
        df_chair2 = df_chair2.dropna(subset=['張地'], axis=0)

        s_chair2 = df_chair2.groupby('張地')['数量'].sum()
        s_chair2.sort_values(ascending=False, inplace=True)

        st.markdown('##### ■ ダイニングチェア')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### 数量')
            graph.make_bar(s_chair2, s_chair2.index) #板座外す
        with col2:
            st.markdown('##### 構成比')
            graph.make_pie(s_chair2, s_chair2.index)
        
        #塗色+張地
        #sofa
        df_sofa2 = df_sofa.copy()
        df_sofa2['塗色/張地'] = df_sofa2['塗色'] + '/' + df_sofa2['張地']
        df_sofa2 = df_sofa2.groupby(['塗色/張地'], as_index=False)['数量'].sum()
        
        df_sofa2.sort_values('数量', ascending=False, inplace=True)

        st.markdown('#### 塗色＋張地別集計/数量 Top10')
        st.markdown('##### ■ ソファ')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### 数量')
            graph.make_bar(df_sofa2['数量'][:10], df_sofa2['塗色/張地'][:10])
        with col2:
            st.markdown('##### 構成比')
            graph.make_pie(df_sofa2['数量'][:10], df_sofa2['塗色/張地'][:10])
        
        #chair
        df_chair2 = df_chair.copy()
        # 空白文字を NaN 値に置き換える
        df_chair2['張地'] = df_chair2['張地'].replace('', np.nan)
        df_chair2 = df_chair2.dropna(subset=['張地'], axis=0)
        
        df_chair2['塗色/張地'] = df_chair2['塗色'] + '/' + df_chair2['張地']
        df_chair2 = df_chair2.groupby(['塗色/張地'], as_index=False)['数量'].sum()
        
        df_chair2.sort_values('数量', ascending=False, inplace=True)

        st.markdown('##### ■ ダイニングチェア')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### 数量')
            graph.make_bar(df_chair2['数量'][:10], df_chair2['塗色/張地'][:10])
        with col2:
            st.markdown('##### 構成比')
            graph.make_pie(df_chair2['数量'][:10], df_chair2['塗色/張地'][:10])


    def series(self, df, graph):
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


    def hinban(self, df, graph):
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

    def association(self, df_selected):

        #************************項目選択
        selected_data = st.selectbox(
            'データ選択',
            ['--', 'フル品番: 例SG261A', '頭品番＋１ケタ: 例SG2'],
            key='sd')

        if selected_data == '--':
            st.info('データを選択してください')
            st.stop()


        elif selected_data == 'フル品番: 例SG261A':

            df_selected['品番2'] = df_selected['商品コード'].map(lambda x:str(x).split(' ')[0])
            df_selected['伝票番号2'] = df_selected['催事見積番号'].map(lambda x:str(x)[0:8])

            temp1 = df_selected.groupby(["伝票番号2", "品番2"])["数量"].sum()

            #行から列へピボット: unstack()
            temp2 = temp1.unstack().fillna(0) 

            association_df = temp2.apply(lambda x: x>0) 

            freq_items1 = apriori(association_df, min_support=0.0005, use_colnames=True) 
            # min_support 閾値 その組み合わせの全体の構成比
            freq_items1.sort_values('support', ascending=False) 

            #■ support 「AとBが一緒にあるデータの数」/「全てのデータ数」
            #■ confidence 商品Aが買われた中で、商品Bも一緒に買われた割合
            #■ lift 「確信度」/「Bの起こる確率」

            df_rules = association_rules(freq_items1, metric='lift', min_threshold=1)
            #liftが1より大きい組み合わせを抽出
            df_rules = df_rules.sort_values('lift', ascending=False)

            with st.expander('項目の説明', expanded=False):
                st.caption('support 「AとBが一緒にあるデータの数」/「全てのデータ数」')
                st.caption('confidence 商品Aが買われた中で、商品Bも一緒に買われた割合')
                st.caption('lift 「確信度」/「Bの起こる確率」')

            selected_cate = st.selectbox(
                '項目選択',
                ['--', '分析一覧を見る', '品番で抽出']
                ,key='sc'
            )

            if selected_cate == '--':
                st.info('項目を選択してください')
                st.stop()

            elif selected_cate == '分析一覧を見る':
                with st.form("入力欄"):
                    lower_antecedent = st.number_input('antecedent support下限')
                    lower_consequent = st.number_input('consequent support下限')
                    lower_lift = st.number_input('lift下限', value=1.5)

                    submitted = st.form_submit_button("Submit")

                    if submitted:
                        df_rules2 = df_rules[(df_rules['antecedent support'] >= lower_antecedent) & \
                                            (df_rules['consequent support'] >= lower_consequent)]
                        df_rules2 = df_rules2[(df_rules2['lift'] >= lower_lift)]

                        
                        st.dataframe(df_rules2)
                        st.write(f'データ数: {len(df_rules2)}')

            elif selected_cate == '品番で抽出':
                selected_item = st.text_input('品番を入力')

                if selected_item == '':
                    st.info('品番を入力してください ※半角英数/アルファベットは大文字　例SG261A')
                    st.stop()

                else:
                    df_rules2 = df_rules[df_rules['antecedents'] ==frozenset({selected_item})]
                    st.dataframe(df_rules2)

        #**********************************************************************************************************
        elif selected_data == '頭品番＋１ケタ: 例SG2':

                df_selected['品番2'] = df_selected['商品コード'].map(lambda x:str(x)[0:3])
                df_selected['伝票番号2'] = df_selected['催事見積番号'].map(lambda x:str(x)[0:8])

                temp1 = df_selected.groupby(["伝票番号2", "品番2"])["数量"].sum()

                #行から列へピボット: unstack()
                temp2 = temp1.unstack().fillna(0) 

                association_df = temp2.apply(lambda x: x>0) 

                freq_items1 = apriori(association_df, min_support=0.0005, use_colnames=True) 
                # min_support 閾値 その組み合わせの全体の構成比
                freq_items1.sort_values('support', ascending=False) 

                #■ support 「AとBが一緒にあるデータの数」/「全てのデータ数」
                #■ confidence 商品Aが買われた中で、商品Bも一緒に買われた割合
                #■ lift 「確信度」/「Bの起こる確率」

                df_rules = association_rules(freq_items1, metric='lift', min_threshold=1)
                #liftが1より大きい組み合わせを抽出
                df_rules = df_rules.sort_values('lift', ascending=False)

                with st.expander('項目の説明', expanded=False):
                    st.caption('support 「AとBが一緒にあるデータの数」/「全てのデータ数」')
                    st.caption('confidence 商品Aが買われた中で、商品Bも一緒に買われた割合')
                    st.caption('lift 「確信度」/「Bの起こる確率」')

                selected_cate = st.selectbox(
                    '項目選択',
                    ['--', '分析一覧を見る', '品番で抽出']
                    ,key='sc2'
                )

                if selected_cate == '--':
                    st.info('項目を選択してください')
                    st.stop()

                elif selected_cate == '分析一覧を見る':
                    with st.form("入力欄"):
                        lower_antecedent = st.number_input('antecedent support下限')
                        lower_consequent = st.number_input('consequent support下限')
                        lower_lift = st.number_input('lift下限', value=1.5)

                        submitted = st.form_submit_button("Submit")

                        if submitted:
                            df_rules2 = df_rules[(df_rules['antecedent support'] >= lower_antecedent) & \
                                                (df_rules['consequent support'] >= lower_consequent)]
                            df_rules2 = df_rules2[(df_rules2['lift'] >= lower_lift)]

                            
                            st.dataframe(df_rules2)
                            st.write(f'データ数: {len(df_rules2)}')

                elif selected_cate == '品番で抽出':
                    selected_item = st.text_input('品番を入力')

                    if selected_item == '':
                        st.info('品番を入力してください ※半角英数/アルファベットは大文字 例SG2')
                        st.stop()

                    else:
                        df_rules2 = df_rules[df_rules['antecedents'] ==frozenset({selected_item})]
                        st.dataframe(df_rules2)

