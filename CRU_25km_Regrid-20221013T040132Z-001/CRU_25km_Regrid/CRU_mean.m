clc
clear all

f1=csvread('NWH-CRU_pre_1901-2021_month_Bicubic_25km.csv');
f2=csvread('NWH-CRU_pre_1901-2021_month_Bilinear_25km.csv');
f3=csvread('NWH-CRU_pre_1901-2021_month_Nearest_25km.csv');
f4=csvread('NWH-CRU_tmn_1901-2021_month_Bicubic_25km.csv');
f5=csvread('NWH-CRU_tmn_1901-2021_month_Bilinear_25km.csv');
f6=csvread('NWH-CRU_tmn_1901-2021_month_Nearest_25km.csv');
f7=csvread('NWH-CRU_tmp_1901-2021_month_Bicubic_25km.csv');
f8=csvread('NWH-CRU_tmp_1901-2021_month_Bilinear_25km.csv');
f9=csvread('NWH-CRU_tmp_1901-2021_month_Nearest_25km.csv');
f10=csvread('NWH-CRU_tmx_1901-2021_month_Bicubic_25km.csv');
f11=csvread('NWH-CRU_tmx_1901-2021_month_Bilinear_25km.csv');
f12=csvread('NWH-CRU_tmx_1901-2021_month_Nearest_25km.csv');

g1=mean(f1(:,3:end)')';
g2=mean(f2(:,3:end)')';
g3=mean(f3(:,3:end)')';
g4=mean(f4(:,3:end)')';
g5=mean(f5(:,3:end)')';
g6=mean(f6(:,3:end)')';
g7=mean(f7(:,3:end)')';
g8=mean(f8(:,3:end)')';
g9=mean(f9(:,3:end)')';
g10=mean(f10(:,3:end)')';
g11=mean(f11(:,3:end)')';
g12=mean(f12(:,3:end)')';

G=[f1(:,1:2),g1,g2,g3,g4,g5,g6,g7,g8,g9,g10,g11,g12];
csvwrite('Mean_CRU_temp_pre_25km.csv',G)
