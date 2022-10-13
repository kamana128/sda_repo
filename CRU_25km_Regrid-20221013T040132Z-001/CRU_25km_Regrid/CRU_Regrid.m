clear all
close all
clc

%%% CRU Monthly 50km during 1901-2021 %%%
% file='cru_ts4.06.1901.2021.pre.dat.nc';
% file='cru_ts4.06.1901.2021.tmn.dat.nc';
% file='cru_ts4.06.1901.2021.tmp.dat.nc';
file='cru_ts4.06.1901.2021.tmx.dat.nc';
% ncdisp(file)

lon = ncread(file,'lon');  % 720 X 1
lat= ncread(file,'lat');  % 360 X 1
time = ncread(file,'time');  % 1452 X 1
% pre = ncread(file,'pre');  % lon X lat X time i.e., 720 X 360 X 1440  Missing value = 9.969209968386869e+36
% new_pre=pre(493:561,193:258,:); % 69 X 66 X 1440  % 66.25-100.25 deg E, 6.25-38.75 deg N
% pre = ncread(file,'tmn');  % lon X lat X time i.e., 720 X 360 X 1440  Missing value = 9.969209968386869e+36
% new_pre=pre(493:561,193:258,:); % 69 X 66 X 1440  % 66.25-100.25 deg E, 6.25-38.75 deg N
% pre = ncread(file,'tmp');  % lon X lat X time i.e., 720 X 360 X 1440  Missing value = 9.969209968386869e+36
% new_pre=pre(493:561,193:258,:); % 69 X 66 X 1440  % 66.25-100.25 deg E, 6.25-38.75 deg N
pre = ncread(file,'tmx');  % lon X lat X time i.e., 720 X 360 X 1440  Missing value = 9.969209968386869e+36
new_pre=pre(493:561,193:258,:); % 69 X 66 X 1440  % 66.25-100.25 deg E, 6.25-38.75 deg N

%%% bicubic
% fname='50_to_25_bicubic'; 
% Method = 'Bicubic';
% Method = 'Bilinear';
Method = 'Nearest';

lat_in = 6.25;
lat_f  = 38.75;
lon_in = 66.25;
lon_f =100.25;
x1=lat_in:0.5:lat_f;
y1=lon_in:0.5:lon_f;
[x2,y2]=meshgrid(y1,x1);

lat_dest_in=6.25;
lat_dest_f=38.75;
lon_dest_in=66.25;
lon_dest_f=100.25;
x1_g=lat_dest_in:0.25:lat_dest_f;
y1_g=lon_dest_in:0.25:lon_dest_f;
[xq,yq]=meshgrid(y1_g,x1_g);

A=[];
for K=1:size(time,1)
    K;
    f=new_pre(:,:,K);
    data1 = interp2(x2,y2,f',xq,yq,Method);
    
    l=1;
    k=1;
    for i = 1:1:131       %%% i represents longitude
        for j = 1:1:137   %%% j represents latitude
            k1=1;
            a(k1,l)=data1(i,j,k);
            k1=k1+1;
            l=l+1;
        end
    end
    a=a';
    A=horzcat(A,a);
    a=[];
end

k=1; 
for i =66.25:0.25:100.25  % Long 
    for j=6.25:0.25:38.75  % Lat
        x_1(k,1)= i;
        x_1(k,2)= j;     %% longitude varies with constant latitude 
        k=k+1;
    end  
end
B=[x_1,A];
% B(B<0)=0; % Remove negative values
B(isnan(B))=0; % Remove NaN values 

grids = x_1;
for i = 1:size(grids)
    for j=1:size(B)
        if((grids(i,1)==B(j,1))&&(grids(i,2)==B(j,2)))
            j;
            arr_data(i,1:size(B,2)-2)=B(j,3:size(B,2));
        end
    end
end
final=[grids,arr_data];
% csvwrite(['Ind-CRU_pre_1901-2021_month_',Method,'_25km.csv'],final)
% csvwrite(['Ind-CRU_tmn_1901-2021_month_',Method,'_25km.csv'],final)
% csvwrite(['Ind-CRU_tmp_1901-2021_month_',Method,'_25km.csv'],final)
csvwrite(['Ind-CRU_tmx_1901-2021_month_',Method,'_25km.csv'],final)

% figure(1);
% surf(x1,y1,f);
% figure(2);
% surf(x1_g,y1_g,data1');

%%%%% NWH %%%%%
y3 = csvread('NWH_25km_grid.csv'); % 25 km NWH grids
x = final;
for i = 1:size(y3)
    for j=1:size(x)
        if((y3(i,1)==x(j,1))&&(y3(i,2)==x(j,2)))
            j
            arr_data1(i,1:size(B,2)-2)=x(j,3:size(B,2));
        end
    end
end
data2=[y3,arr_data1];
% csvwrite(['NWH-CRU_pre_1901-2021_month_',Method,'_25km.csv'],data2)
% csvwrite(['NWH-CRU_tmn_1901-2021_month_',Method,'_25km.csv'],data2)
% csvwrite(['NWH-CRU_tmp_1901-2021_month_',Method,'_25km.csv'],data2)
csvwrite(['NWH-CRU_tmx_1901-2021_month_',Method,'_25km.csv'],data2)

