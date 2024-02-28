import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title='Rayhan - Capstone Project Tetris Batch 4',
    layout='wide'
) 

df = pd.read_csv('data_year.csv')
df['tahun'] = df['tahun'].astype(str)

# Sidebar
tahun_list = df['tahun'].unique()
selected_tahun = st.sidebar.selectbox('Pilih tahun', tahun_list)

df_tahun= df[df['tahun'] == f'{selected_tahun}']

st.sidebar.header('Hipotesis dari sumber Berita')
st.sidebar.image('berita.png', use_column_width=True)
st.sidebar.image('berita3.jpg', use_column_width=True)
st.sidebar.image('berita2.png', use_column_width=True)

# Judul
st.title('Analisis Angka Harapan Hidup, Pengeluaran, dan Jumlah Penduduk Miskin di Jawa Barat')
st.write('''
         Beberapa berita menyebutkan bahwa angka harapan hidup di Kabupaten Cianjur adalah nomor 2 terendah
         dari sekian banyak Kabupaten dan Kota di Jawa Barat. Serta jumlah penduduk miskin di Jawa Barat yang mencapai 4 juta penduduk. 
         Mari kita cek data yang ada untuk melihat apakah hal tersebut benar.
         
         Data yang diambil bersumber dari:
         - Open Data Jabar https://opendata.jabarprov.go.id/
         - Badan Pusat Statistik Jawa Barat https://jabar.bps.go.id/
         - Badan Pusat Statistik Kabupaten Bandung https://bandungkab.bps.go.id/
         ''')

# daftar kolom kuantitatif
kolom_kuantitatif = df_tahun.select_dtypes(include='number').columns
# kolom_kuantitatif

# Korelasi antara kolom numerik
correlation_table = df_tahun[kolom_kuantitatif].corr()
# correlation_table

st.subheader('Analisis Data:')
tab_1, tab_2, tab_4, tab_3 = st.tabs(['Harapan Hidup', 'Pengeluaran Per Kapita','Penduduk Miskin', 'Jumlah Penduduk'])

st.divider()

tab_resume, tab_korelasi, tab_data = st.tabs(['Kesimpulan', 'Korelasi', 'Data dan Kamus Data'])

#helper function
def format_big_number(num):
    if num >= 1e6:
        return f"{num / 1e6:.2f} Juta"
    elif num >= 1e3:
        return f"{num / 1e3:.2f} Ribu"
    else:
        return f"{num:.2f}"

with tab_resume:
    #total harapan hidup
    rata_hidup = df_tahun['harapan_hidup'].mean()

    # total pengeluaran
    rata_pengeluaran = df_tahun['pengeluaran_semua'].mean()

    # total penduduk
    jumlah_pdk = df_tahun['jumlah_pdk'].sum()

    # total penduduk miskin
    jumlah_penmiskin = df_tahun['jumlah_penmiskin'].sum()

    # persen penduduk miskin
    persen_jumlah_penmiskin = jumlah_penmiskin / jumlah_pdk * 100

    # total dokter
    jumlah_dokter = df_tahun['jumlah_dokter'].sum()

    # persen penduduk miskin
    persen_dokter = jumlah_dokter / jumlah_pdk * 100

    # hasil perhitungan
    st.subheader('Kesimpulan: ')
    st.write(f'1. Pada tahun {selected_tahun}, rata-rata angka harapan hidup penduduk di Jawa Barat adalah {round(rata_hidup, 2)} tahun.')
    st.write(f"2. Rata-rata pengeluaran per kapita penduduk di Jawa Barat adalah Rp {round(rata_pengeluaran):,}.")
    st.write(f'3. Total penduduk di Jawa Barat pada tahun {selected_tahun} adalah {format_big_number(jumlah_pdk)} Jiwa.')
    st.write(f'4. Total penduduk miskin di Jawa Barat pada tahun {selected_tahun} adalah {format_big_number(jumlah_penmiskin)} atau {round(persen_jumlah_penmiskin, 2)}% dari total penduduk.')
    st.write(f'5. Total dokter umum di Jawa Barat pada tahun {selected_tahun} adalah {jumlah_dokter} atau {round(persen_dokter, 2)}% dari total penduduk.')
    
    # resume korelasi
    corr_harapan_pengeluaran = correlation_table.loc['harapan_hidup', 'pengeluaran_semua']
    st.write(f'6. Korelasi antara angka harapan hidup dengan pengeluaran per kapita ({corr_harapan_pengeluaran:.3f}).Ini berarti bahwa semakin tinggi pengeluaran per kapita, semakin tinggi pula harapan hidup.')

    correlation_harapan_kepadatan = correlation_table.loc['harapan_hidup', 'kepadatan_pdk']
    correlation_harapan_garmiskin = correlation_table.loc['harapan_hidup', 'garis_kemiskinan']
    st.write(f'7. Angka harapan hidup juga memiliki korelasi positif yang kuat dengan kepadatan penduduk ({correlation_harapan_kepadatan:.3f}) dan garis kemiskinan ({correlation_harapan_garmiskin:.3f}). Ini menunjukkan bahwa semakin tinggi kepadatan penduduk dan garis kemiskinan, semakin tinggi pula harapan hidup.')

with tab_korelasi:
    st.subheader('Korelasi antar variabel:')

    correlation_table = df_tahun[['harapan_hidup', 'pengeluaran_semua', 'kepadatan_pdk', 'garis_kemiskinan', 'jumlah_dokter', 'jumlah_pdk', 'jumlah_rumtang', 'jumlah_penmiskin']].corr()
    # correlation_table
    fig = px.imshow(correlation_table, color_continuous_scale='RdBu', title='Heatmap')
    st.plotly_chart(fig)

with tab_data:
    st.subheader('Kamus Data')
    kamus = '''
    "wilayah": Nama wilayah kabupaten/kota.
    "tahun": Tahun dimana data itu diambil.
    "harapan_hidup": Rata-rata harapan hidup untuk semua populasi.
    "harapan_hidup_L": Rata-rata harapan hidup untuk populasi laki-laki.
    "harapan_hidup_P": Rata-rata harapan hidup untuk populasi perempuan.
    "pengeluaran_semua": Pengeluaran rata-rata per kapita untuk semua jenis pengeluaran dalam satuan Rupiah.
    "pengeluaran_makanan": Pengeluaran rata-rata per kapita khusus untuk pengeluaran makanan dalam satuan Rupiah.
    "pengeluaran_nonmakanan": Pengeluaran rata-rata per kapita untuk semua jenis pengeluaran kecuali makanan dalam satuan Rupiah.
    "jumlah_pdk": Total Jumlah penduduk.
    "jumlah_pdk_L": Jumlah penduduk laki-laki.
    "jumlah_pdk_P": Jumlah penduduk perempuan.
    "jumlah_rumtang": Jumlah rumah tangga.
    "jumlah_penmiskin": Jumlah penduduk miskin.
    "jumlah_dokter": Jumlah dokter umum.
    "kepadatan_pdk": Kepadatan penduduk dalam satuan Jiwa per Kilometer persegi.
    "garis_kemiskinan": Garis kemiskinan dalam satuan Rupiah.
    '''
    
    for line in kamus.strip().split('\n'):
        st.write(line)

    st.divider()
    
    st.subheader('Data')
    df
    
with tab_1:
    # grafik semua
    df_sorted = df_tahun.sort_values('harapan_hidup', ascending=True)
    # Bar plot
    fig = px.bar(df_sorted, x='harapan_hidup', y='wilayah', 
                 labels={'harapan_hidup': 'Harapan Hidup (Umur)', 'wilayah': 'Wilayah'},
                 title=f'Distribusi Harapan Hidup (Umur) setiap kab/kota di Jawa Barat pada tahun {selected_tahun}')
    st.plotly_chart(fig)
    
    # rata harapan hidup
    rata_hidup_L = df_tahun['harapan_hidup_L'].mean()
    rata_hidup_P = df_tahun['harapan_hidup_P'].mean()

    # pie chart
    df_pie = pd.DataFrame({'Jenis Kelamin': ['Laki-laki', 'Perempuan'], 'Rata-rata Harapan Hidup': [round(rata_hidup_L, 2), round(rata_hidup_P, 2)]})
    fig = px.pie(df_pie, values='Rata-rata Harapan Hidup', names='Jenis Kelamin', title=f'Perbandingan Rata-rata Harapan Hidup Laki-laki dan Perempuan pada tahun {selected_tahun}')
    st.plotly_chart(fig)
    
    
    # Hitung total harapan hidup
    df_tahun['total_harapan_hidup'] = df_tahun['harapan_hidup_L'] + df_tahun['harapan_hidup_P']

    # Hitung persentase harapan hidup laki-laki dan perempuan
    df_tahun['persen_hidup_L'] = df_tahun['harapan_hidup_L'] / df_tahun['total_harapan_hidup'] * 100
    df_tahun['persen_hidup_P'] = df_tahun['harapan_hidup_P'] / df_tahun['total_harapan_hidup'] * 100

    # Buat bar plot untuk persentase harapan hidup laki-laki dan perempuan
    fig = px.bar(df_tahun, y='wilayah', x=['persen_hidup_L', 'persen_hidup_P'], 
                labels={'value': 'Persentase', 'wilayah': 'Wilayah', 'variable': 'Jenis Kelamin'},
                title=f'Perbandingan Persentase Harapan Hidup Laki-laki dan Perempuan setiap kab/kota di Jawa Barat pada tahun {selected_tahun}')
    st.plotly_chart(fig)
    
with tab_2:
    # Hitung total pengeluaran
    df_tahun['pengeluaran_semua'] = df_tahun['pengeluaran_makanan'] + df_tahun['pengeluaran_nonmakanan']

    # Grafik semua
    df_sorted = df_tahun.sort_values('pengeluaran_semua', ascending=True)
    # Bar plot
    fig = px.bar(df_sorted, x='pengeluaran_semua', y='wilayah', 
                 labels={'pengeluaran_semua': 'Pengeluaran Per Kapita', 'wilayah': 'Wilayah'},
                 title=f'Distribusi Pengeluaran Per Kapita setiap kab/kota di Jawa Barat pada tahun {selected_tahun}')
    st.plotly_chart(fig)

    # rata-rata pengeluaran
    rata_pengeluaran_makanan = df_tahun['pengeluaran_makanan'].mean()
    rata_pengeluaran_nonmakanan = df_tahun['pengeluaran_nonmakanan'].mean()

    # pie chart
    df_pie = pd.DataFrame({'Jenis Pengeluaran': ['Makanan', 'Non-Makanan'], 'Rata-rata Pengeluaran': [round(rata_pengeluaran_makanan, 2), round(rata_pengeluaran_nonmakanan, 2)]})
    fig = px.pie(df_pie, values='Rata-rata Pengeluaran', names='Jenis Pengeluaran', title=f'Perbandingan Rata-rata Pengeluaran Makanan dan Non-Makanan')
    st.plotly_chart(fig)

    # persen pengeluaran
    df_tahun['persen_pengeluaran_makanan'] = df_tahun['pengeluaran_makanan'] / df_tahun['pengeluaran_semua'] * 100
    df_tahun['persen_pengeluaran_nonmakanan'] = df_tahun['pengeluaran_nonmakanan'] / df_tahun['pengeluaran_semua'] * 100

    # bar plot
    fig = px.bar(df_tahun, y='wilayah', x=['persen_pengeluaran_makanan', 'persen_pengeluaran_nonmakanan'], 
                 labels={'value': 'Persentase', 'wilayah': 'Wilayah', 'variable': 'Jenis Pengeluaran'},
                 title=f'Perbandingan Persentase Pengeluaran Makanan dan Non-Makanan')
    st.plotly_chart(fig)
    
with tab_3:
    #total penduduk
    df_tahun['jumlah_pdk'] = df_tahun['jumlah_pdk_L'] + df_tahun['jumlah_pdk_P']

    df_sorted = df_tahun.sort_values('jumlah_pdk', ascending=True)
    # Bar plot
    fig = px.bar(df_sorted, x='jumlah_pdk', y='wilayah', 
                 labels={'jumlah_pdk': 'Jumlah Penduduk', 'wilayah': 'Wilayah'},
                 title=f'Distribusi Jumlah Penduduk setiap kab/kota di Jawa Barat pada tahun {selected_tahun}')
    st.plotly_chart(fig)

    # jumlah penduduk laki-laki dan perempuan
    jumlah_pdk_L = df_tahun['jumlah_pdk_L'].sum()
    jumlah_pdk_P = df_tahun['jumlah_pdk_P'].sum()

    # pie chart
    df_pie = pd.DataFrame({'Jenis Kelamin': ['Laki-laki', 'Perempuan'], 'Jumlah Penduduk': [round(jumlah_pdk_L, 2), round(jumlah_pdk_P, 2)]})
    fig = px.pie(df_pie, values='Jumlah Penduduk', names='Jenis Kelamin', title=f'Perbandingan Jumlah Penduduk Laki-laki dan Perempuan pada tahun {selected_tahun}')
    st.plotly_chart(fig)

    # persen penduduk laki-laki dan perempuan
    df_tahun['persen_pdk_L'] = df_tahun['jumlah_pdk_L'] / df_tahun['jumlah_pdk'] * 100
    df_tahun['persen_pdk_P'] = df_tahun['jumlah_pdk_P'] / df_tahun['jumlah_pdk'] * 100

    # bar plot
    fig = px.bar(df_tahun, y='wilayah', x=['persen_pdk_L', 'persen_pdk_P'], 
                 labels={'value': 'Persentase', 'wilayah': 'Wilayah', 'variable': 'Jenis Kelamin'},
                 title=f'Perbandingan Persentase Penduduk Laki-laki dan Perempuan setiap kab/kota di Jawa Barat pada tahun {selected_tahun}')
    st.plotly_chart(fig)

with tab_4:
    df_sorted = df_tahun.sort_values('jumlah_pdk', ascending=True)
    # Grafik jumlah penduduk dan jumlah penduduk miskin
    fig = px.bar(df_sorted, x=['jumlah_pdk', 'jumlah_penmiskin'], y='wilayah',
                 labels={'value': 'Jumlah', 'wilayah': 'Wilayah', 'variable': 'Jenis'},
                 title=f'Distribusi Jumlah Penduduk dan Jumlah Penduduk Miskin setiap kab/kota di Jawa Barat pada tahun {selected_tahun}')
    st.plotly_chart(fig)
    
    # jumlah penduduk miskin
    jumlah_penmiskin = df_tahun['jumlah_penmiskin'].sum()

    # persen penduduk miskin
    persen_penmiskin = jumlah_penmiskin / jumlah_pdk * 100

    #pie chart
    df_pie = pd.DataFrame({'Jenis': ['Penduduk Miskin', 'Penduduk Tidak Miskin'], 'Jumlah': [jumlah_penmiskin, jumlah_pdk - jumlah_penmiskin]})
    fig = px.pie(df_pie, values='Jumlah', names='Jenis', title=f'Perbandingan Jumlah Penduduk Miskin dan Non-Penduduk Miskin pada tahun {selected_tahun}')
    st.plotly_chart(fig)
    
st.markdown('''<div style="text-align: center;">
            © 2024 Muhammad Rayhan Kurniawan | <a href="https://www.linkedin.com/in/mrayhankurniawan/">LinkedIn</a></div>''',
            unsafe_allow_html=True)
