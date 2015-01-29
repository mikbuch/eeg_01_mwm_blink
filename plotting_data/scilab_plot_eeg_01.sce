////////////////////////////////////////////
//                                        //
// This script operates on data           //
// from a 1-electrode EEG                 //
//                                        //
////////////////////////////////////////////

////////////////////////////////
//   variables declaration    //
////////////////////////////////

//// create variable EEGdata
// // create varibales from csv files
eeg_data_01=csvRead("../csv_eeg_ann/scilab_eeg_01_sub_001.csv");
eeg_data_02=csvRead("../csv_eeg_ann/scilab_eeg_01_sub_002.csv");
eeg_data_03=csvRead("../csv_eeg_ann/scilab_eeg_01_sub_003.csv");

plots_width=2200;
plots_heigth=1700;


////////////////////////////////
//       plotting data        //
////////////////////////////////

////////////////
//  sub_001   //
////////////////

f1=scf(1);
f=get("current_figure") 
f.figure_size=[plots_width,plots_heigth]
a=gca();  
a.font_size=5;
p=get("hdl");
title("Wyniki osoby badanej 001","fontsize",6);
xlabel("próbka sygnału (512/sekundę)","fontsize",5);
ylabel("amplituda sygnału (µV), bodziec oraz kategoryzacja","fontsize",5);
// plotting raw signal 
plot(eeg_data_01(:,1))
// plotting stimulus
p.thickness=10;
plot(eeg_data_01(:,2), '-k')
// plotting categorization
p.thickness=3;
plot(eeg_data_01(:,3), '-r')

////////////////
//  sub_002   //
////////////////

f1=scf(2);
f=get("current_figure") 
f.figure_size=[plots_width,plots_heigth]
a=gca();  
a.font_size=5;
p=get("hdl");
title("Wyniki osoby badanej 002","fontsize",6);
xlabel("próbka sygnału (512/sekundę)","fontsize",5);
ylabel("amplituda sygnału (µV), bodziec oraz kategoryzacja","fontsize",5);
// plotting raw signal 
plot(eeg_data_02(:,1))
// plotting stimulus
p.thickness=10;
plot(eeg_data_02(:,2), '-k')
// plotting categorization
p.thickness=3;
plot(eeg_data_02(:,3), '-r')

////////////////
//  sub_003   //
////////////////

f1=scf(3);
f=get("current_figure") 
f.figure_size=[plots_width,plots_heigth]
a=gca();  
a.font_size=5;
p=get("hdl");
title("Wyniki osoby badanej 003","fontsize",6);
xlabel("próbka sygnału (512/sekundę)","fontsize",5);
ylabel("amplituda sygnału (µV), bodziec oraz kategoryzacja","fontsize",5);
// plotting raw signal 
plot(eeg_data_03(:,1))
// plotting stimulus
p.thickness=10;
plot(eeg_data_03(:,2), '-k')
// plotting categorization
p.thickness=3;
plot(eeg_data_03(:,3), '-r')


////////////////////////////////
//      exporting data        //
////////////////////////////////

xs2pdf(1,'scilab_eeg_01_sub_001.pdf');
xs2pdf(2,'scilab_eeg_01_sub_002.pdf');
xs2pdf(3,'scilab_eeg_01_sub_003.pdf');
