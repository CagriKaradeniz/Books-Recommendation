import pandas as pd
import numpy as np
from PIL import Image
from imageio import imread
import urllib.request
from PIL import Image
import matplotlib.pyplot as plt
import requests
import Utils_cagri as util
from mlxtend.frequent_patterns import apriori, association_rules
pd.set_option('display.max_columns', 20)
pd.set_option('display.expand_frame_repr', False)

books=pd.read_csv("Book Recommendation Dataset/Books.csv")
rating=pd.read_csv("Book Recommendation Dataset/Ratings.csv")
users=pd.read_csv("Book Recommendation Dataset/Users.csv")


data=rating.merge(users,on="User-ID")
data=data.merge(books,on="ISBN")
data.drop(columns=["Image-URL-S","Image-URL-M"],inplace=True)
data["Age"]=data["Age"].fillna(data["Age"].mode()[0])
r={}
for i,j in enumerate(data["Book-Title"].unique()):
    r[j]=i
data["Book-ID"]=data["Book-Title"].map(r)
random_user=int(data["User-ID"].sample(1,random_state=40))


def item_based_recommender(kitap, data):
    kitap_ad = data[kitap]
    return data.corrwith(kitap_ad).sort_values(ascending=False).head(10)

def kullanıcıBased_dataolustur(df):
    comment_counts = pd.DataFrame(df["Book-Title"].value_counts())
    rare_movies = comment_counts[comment_counts["Book-Title"] <= 50].index
    common_movies = df[~df["Book-Title"].isin(rare_movies)]
    user_movie_df = common_movies.pivot_table(index=["User-ID"], columns=["Book-Title"], values="Book-Rating")
    return user_movie_df

def kitap_tavsiye(data):
    yontem=int(input("Tavsiye yöntemini Seçiniz (1=Kitap tabanlı tavsiye, 2=Kullanıcı tabanlı tavsiye) :"))
    if yontem==1:
        kit_ad=str(input("Listede bulunan ve beğendiğin bir kitabın ismini gir:"))
        print(kit_ad,type(kit_ad))
        if sum(data["Book-Title"].astype("str").str.contains(kit_ad)) == 0:
            print("Üzgünüz listede olmayan kitap seçimi yaptınız....")
        else:

            user_data = kullanıcıBased_dataolustur(data)
            kitaplar=item_based_recommender(kit_ad, user_data).index[0:2].tolist()
            print(kitaplar,type(kitaplar))
            url0 = data[data["Book-Title"]==kitaplar[0]]["Image-URL-L"].to_list()[0]
            url1 = data[data["Book-Title"]==kitaplar[1]]["Image-URL-L"].to_list()[0]
            im0 = imread(url0)
            im1 = imread(url1)
            plt.figure(1)
            plt.axis(False)
            plt.imshow(im0)
            plt.figure(2)
            plt.axis(False)
            plt.imshow(im1)
    elif yontem==2:
        Id=int(input("Kullanıcı ID numaranızı giriniz : "))
        if sum(data["User-ID"].astype("str").str.contains(str(Id))) == 0:
            print("Üzgünüz listede olmayan bir kullanıcı ID'si girdiniz....")
        else:
            user_data = kullanıcıBased_dataolustur(data)
            okunan_kitap_df = user_data[user_data.index == Id]
            okunan_kitap_list = okunan_kitap_df.columns[okunan_kitap_df.notna().any()].tolist()
            okunan_kitap_data = user_data[okunan_kitap_list]
            okunan_kitap_sayi = okunan_kitap_data.T.notnull().sum()
            okunan_kitap_sayi = okunan_kitap_sayi.reset_index()
            okunan_kitap_sayi.columns = ["userId", "kitap_sayısı"]
            sayi = len(okunan_kitap_list) * 60 / 100
            benzer_okuyan_kullanicilar = okunan_kitap_sayi[okunan_kitap_sayi["kitap_sayısı"] > sayi]["userId"]
            final_data = pd.concat([okunan_kitap_data[okunan_kitap_data.index.isin(benzer_okuyan_kullanicilar)],
                                    okunan_kitap_df[okunan_kitap_list]])
            corr_data = final_data.T.corr().unstack().sort_values().drop_duplicates()
            corr_data = pd.DataFrame(corr_data, columns=["Corr"])
            corr_data.index.names = ["user_id_1", "user_id_2"]
            corr_data = corr_data.reset_index()
            benzer_kullanicilar = \
                corr_data[(corr_data["user_id_2"] == Id) & (corr_data["Corr"] > 0)].sort_values("Corr",
                                                                                                ascending=False)[
                    ["user_id_1", "Corr"]]
            benzer_kullanicilar.rename(columns={"user_id_1": "User-ID"}, inplace=True)
            benzer_kullanicilar_rating = benzer_kullanicilar.merge(data[["User-ID", "Book-ID", "Book-Rating"]],
                                                                   how="inner")
            benzer_kullanicilar_rating = benzer_kullanicilar_rating[benzer_kullanicilar_rating["User-ID"] != Id]
            benzer_kullanicilar_rating["Weighted_Avarage_Recommendadtion"] = benzer_kullanicilar_rating["Corr"] * \
                                                                             benzer_kullanicilar_rating["Book-Rating"]
            top_df = benzer_kullanicilar_rating.groupby("Book-ID").agg({"Weighted_Avarage_Recommendadtion": "mean"}). \
                sort_values("Weighted_Avarage_Recommendadtion", ascending=False)
            top_df = top_df.reset_index()
            user_based = top_df.merge(data[["Book-ID", "Book-Title"]], on="Book-ID")["Book-Title"].head(2)
            print(user_based)
            url0 = data[data["Book-Title"] == user_based[0]]["Image-URL-L"].to_list()[0]
            url1 = data[data["Book-Title"] == user_based[1]]["Image-URL-L"].to_list()[0]
            im0 = imread(url0)
            im1 = imread(url1)
            plt.figure(1)
            plt.axis(False)
            plt.imshow(im0)
            plt.figure(2)
            plt.axis(False)
            plt.imshow(im1)

    else:
        print("Yanlış giriş yaptınız ")




kitap_tavsiye(data)





