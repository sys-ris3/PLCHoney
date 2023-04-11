FUNCTION_BLOCK Parameter_Array
  VAR_OUTPUT
    min_green_arr : ARRAY [1..6] OF TIME := [T#8s, T#6s, T#0s, T#0s, T#8s, T#5s];
    max_green_arr : ARRAY [1..6] OF TIME := [T#30s, T#14s, T#0s, T#30s, T#20s, T#12s];
    veh_ext_arr : ARRAY [1..6] OF TIME := [T#2s, T#2s, T#0s, T#0s, T#3s, T#3s];
    yellow_cl_arr : ARRAY [1..6] OF TIME := [T#3s500ms, T#3s500ms, T#0s, T#3s500ms, T#3s500ms, T#3s];
    red_cl_arr : ARRAY [1..6] OF TIME := [T#2s, T#5s, T#3s, T#3s, T#5s, T#3s];
    walk_sec_arr : ARRAY [1..6] OF TIME := [T#7s, T#0s, T#7s, T#0s, T#7s, T#7s];
    ped_cl_arr : ARRAY [1..6] OF TIME := [T#7s, T#0s, T#6s, T#0s, T#6s, T#6s];
  END_VAR
  VAR
    tmp : BOOL;
  END_VAR

  tmp := False;
END_FUNCTION_BLOCK

FUNCTION_BLOCK Phase_One
  VAR_INPUT
    Veh_Cnt : INT;
    Ped_Pressed : BOOL;
    Green_min_1 : BOOL;
    Green_max_1 : BOOL;
    Ped_1 : BOOL;
    Yellow_1 : BOOL;
    Red_1 : BOOL;
  END_VAR
  VAR_OUTPUT
    W_G : BOOL;
    E_G : BOOL;
    E_P : BOOL;
    W_Y : BOOL;
    E_Y : BOOL;
    W_R : BOOL;
    E_R : BOOL;
    N_R : BOOL;
    S_R : BOOL;
    E_LR : BOOL;
    End_of_green : BOOL;
  END_VAR
  VAR
    pars : Parameter_Array;
    veh_total : INT;
    veh_total_prev : INT := 0;
    TON_Veh_ext : TON;
    TON_Ped_ext : TON;
    start_veh_TON : BOOL := False;
    start_ped_TON : BOOL := False;
  END_VAR

  start_veh_TON := Red_1;
  start_ped_TON := Red_1;
  (* vehical extends green: MAX/PED mode *)
  veh_total := MUL(Veh_cnt, TIME_TO_INT(pars.veh_ext_arr[1])); 
  IF veh_total > veh_total_prev THEN
    TON_Veh_ext(IN := AND(NOT(start_veh_TON), Green_min_1), PT := INT_TO_TIME(veh_total - veh_total_prev));
  END_IF;
  veh_total_prev := veh_total;
  
  (* NS_Green_On detects if the current green is still ON *)
  (* Ped clearance can extend to end of green *)
  TON_Ped_ext(IN := AND(NOT(start_ped_TON), Ped_1, Ped_Pressed), PT := pars.ped_cl_arr[1]);
  End_of_green := AND(Green_min_1, OR(AND(TON_Veh_ext.Q, TON_Ped_ext.Q), Green_max_1)); 

  W_G := NOT(End_of_green);
  E_G := NOT(End_of_green);
  (* This ped light cannot extend to yellow, only the end of green *)
  E_P := AND(OR(NOT(Ped_1), LT(TON_Ped_ext.ET,TON_Ped_ext.PT)), NOT(End_of_green));

  W_Y := AND(End_of_green, NOT(Yellow_1));
  E_Y := AND(End_of_green, NOT(Yellow_1));

  W_R := AND(Yellow_1, NOT(Red_1));
  E_R := AND(Yellow_1, NOT(Red_1));
  N_R := True;
  S_R := True;
  E_LR := True;
END_FUNCTION_BLOCK

FUNCTION_BLOCK Phase_Two
  VAR_INPUT
    Green_min_2 : BOOL;
    Green_max_2 : BOOL;
    Veh_cnt : INT;
    Ped_2 : BOOL;
    Ped_Pressed : BOOL;
    Yellow_2 : BOOL;
    Red_2 : BOOL;
  END_VAR
  VAR_OUTPUT
    N_G : BOOL;
    S_G : BOOL;
    N_LG : BOOL;
    N_P : BOOL;
    S_P : BOOL;
    N_Y : BOOL;
    S_Y : BOOL;
    N_LY : BOOL;
    N_R : BOOL;
    S_R : BOOL;
    W_R : BOOL;
    E_R : BOOL;
    E_LR : BOOL;
    End_of_green : BOOL := False;
  END_VAR
  VAR
    pars : Parameter_Array;
    veh_total : INT;
    veh_total_prev : INT;
    start_veh_TON : BOOL := False;
    TON_Veh_ext : TON;
  END_VAR

  (* Second Phase *) 
  start_veh_TON := Red_2;

  (* vehical extends green: MAX/PED mode *)
  veh_total := MUL(Veh_cnt, TIME_TO_INT(pars.veh_ext_arr[2])); 
  IF veh_total > veh_total_prev THEN
    TON_Veh_ext(IN := AND(NOT(start_veh_TON), Green_min_2), PT := INT_TO_TIME(veh_total - veh_total_prev));
  END_IF;
  veh_total_prev := veh_total;
  End_of_green := AND(Green_min_2, OR(TON_Veh_ext.Q, Green_max_2)); 

  N_G := NOT(End_of_green);
  N_LG := NOT(End_of_green);
  N_Y := AND(End_of_green, NOT(Yellow_2));
  N_LY := AND(End_of_green, NOT(Yellow_2));
  N_R := AND(Yellow_2, NOT(Red_2));

  W_R := True;
  E_R := True;
  E_LR := True;
  S_R := True;

END_FUNCTION_BLOCK

FUNCTION_BLOCK Phase_Three
  VAR_OUTPUT
    N_R : BOOL;
    S_R : BOOL;
    W_R : BOOL;
    E_R : BOOL;
    E_LR : BOOL;
    W_P : BOOL;
  END_VAR

  W_P := True;
  N_R := True;
  S_R := True;
  W_R := True;
  E_R := True;
  E_LR := True;
END_FUNCTION_BLOCK

FUNCTION_BLOCK Phase_Five
  VAR_INPUT
    Veh_Cnt : INT;
    Red_5 : BOOL;
    Green_min_5 : BOOL;
    Green_max_5 : BOOL;
    Yellow_5 : BOOL;
    Ped_Pressed : BOOL;
    Ped_5 : BOOL;
    End_Cycle : TIME;
  END_VAR
  VAR_OUTPUT
    N_G : BOOL;
    S_G : BOOL;
    S_P : BOOL;
    N_Y : BOOL;
    S_Y : BOOL;
    N_R : BOOL;
    S_R : BOOL;
    W_R : BOOL;
    E_LR : BOOL;
    E_R : BOOL;
    End_of_Green : BOOL := False;
  END_VAR
  VAR
    pars : Parameter_Array;
    veh_total : INT;
    veh_total_prev : INT;
    start_veh_TON : BOOL;
    start_ped_TON : BOOL;
    TON_Veh_ext : TON;
    TON_Ped_ext : TON;
  END_VAR

  (* Fifth Phase *)
  start_veh_TON := Red_5;
  start_ped_TON := Red_5;
  (* vehical extends green: MAX/PED mode *)
  veh_total := MUL(Veh_cnt, TIME_TO_INT(pars.veh_ext_arr[5])); 
  IF veh_total > veh_total_prev THEN
    TON_Veh_ext(IN := AND(NOT(start_veh_TON), Green_min_5), PT := INT_TO_TIME(veh_total - veh_total_prev));
  END_IF;
  veh_total_prev := veh_total;

  (* NS_Green_On detects if the current green is still ON *)
  (* Ped clearance can extend to end of yellow *)
  TON_Ped_ext(IN := AND(NOT(start_ped_TON), Ped_5, Ped_Pressed), PT := pars.ped_cl_arr[5]);
  End_of_green := AND(Green_min_5, OR(AND(TON_Veh_ext.Q, TON_Ped_ext.Q), Green_max_5)); 

  IF AND(Green_min_5, LE(End_Cycle, pars.yellow_cl_arr[5] + pars.red_cl_arr[5])) THEN
    End_of_Green := True;
  END_IF;

  N_G := NOT(End_of_Green);
  S_G := NOT(End_of_Green);
  S_P := AND(OR(NOT(Ped_5), LT(TON_Ped_ext.ET,TON_Ped_ext.PT)), NOT(Yellow_5));
  N_Y := AND(End_of_Green, NOT(Yellow_5));
  S_Y := AND(End_of_Green, NOT(Yellow_5));
  N_R := AND(Yellow_5, NOT(Red_5));
  S_R := AND(Yellow_5, NOT(Red_5));

  E_LR := True;
  E_R := True;
  W_R := True;
END_FUNCTION_BLOCK


FUNCTION_BLOCK Phase_Six
  VAR_INPUT
    Green_6 : BOOL;
    Yellow_6 : BOOL;
    Red_6 : BOOL;
    Ped_Pressed : BOOL;
    Ped_6 : BOOL;
    End_Cycle : TIME;
  END_VAR
  VAR_OUTPUT
    E_G : BOOL;
    E_LG : BOOL;
    N_P : BOOL;
    E_Y : BOOL;
    E_LY : BOOL;
    E_R : BOOL;
    E_LR : BOOL;
    W_R : BOOL;
    N_R : BOOL;
    S_R : BOOL;
    End_of_Green : BOOL := False;
  END_VAR
  VAR
    pars : Parameter_Array;
    start_ped_TON : BOOL;
    TON_Ped_ext : TON;
  END_VAR

  (* Sixth Phase*)
  start_ped_TON := Red_6;

  (* Ped clearance can extend to end of yellow *)
  TON_Ped_ext(IN := AND(NOT(start_ped_TON), Ped_Pressed, Ped_6), PT := pars.ped_cl_arr[6]);
  End_of_green := False; 
  IF AND(Green_6, LE(End_Cycle, pars.yellow_cl_arr[6] + pars.red_cl_arr[6])) THEN
    End_of_Green := True;
  END_IF;

  E_G := NOT(End_of_Green);
  E_LG := NOT(End_of_Green);
  N_P := AND(OR(NOT(Ped_6), LT(TON_Ped_ext.ET,TON_Ped_ext.PT)), NOT(Yellow_6));
  E_Y := AND(End_of_Green, NOT(Yellow_6));
  E_LY := AND(End_of_Green, NOT(Yellow_6));
  E_R := AND(Yellow_6, NOT(Red_6));
  E_LR := AND(Yellow_6, NOT(Red_6));

  W_R := True;
  N_R := True;
  S_R := True;
END_FUNCTION_BLOCK


FUNCTION_BLOCK Clear_States
  VAR_OUTPUT
    N_G : BOOL;
    S_G : BOOL;
    E_G : BOOL;
    W_G : BOOL;
    N_Y : BOOL;
    S_Y : BOOL;
    E_Y : BOOL;
    W_Y : BOOL;
    N_R : BOOL;
    S_R : BOOL;
    E_R : BOOL;
    W_R : BOOL;
    N_LY : BOOL;
    S_LY : BOOL;
    E_LY : BOOL;
    W_LY : BOOL;
    N_LG : BOOL;
    S_LG : BOOL;
    E_LG : BOOL;
    W_LG : BOOL;
    N_LR : BOOL;
    S_LR : BOOL;
    E_LR : BOOL;
    W_LR : BOOL;
    N_P : BOOL;
    S_P : BOOL;
    E_P : BOOL;
    W_P : BOOL;
  END_VAR

  N_G := False;
  S_G := False;
  E_G := False;
  W_G := False;
  N_Y := False;
  S_Y := False;
  E_Y := False;
  W_Y := False;
  N_R := False;
  S_R := False;
  E_R := False;
  W_R := False;
  N_LY := False;
  S_LY := False;
  E_LY := False;
  W_LY := False;
  N_LG := False;
  S_LG := False;
  E_LG := False;
  W_LG := False;
  N_LR := False;
  S_LR := False;
  E_LR := False;
  W_LR := False;
  N_P := False;
  S_P := False;
  E_P := False;
  W_P := False;
END_FUNCTION_BLOCK


PROGRAM Ruggles_Street
  VAR
    N_G AT %QX0.0 : BOOL;
    S_G AT %QX0.1 : BOOL;
    E_G AT %QX0.2 : BOOL;
    W_G AT %QX0.3 : BOOL;
    N_Y AT %QX0.4 : BOOL;
    S_Y AT %QX0.5 : BOOL;
    E_Y AT %QX0.6 : BOOL;
    W_Y AT %QX0.7 : BOOL;
    N_R AT %QX1.0 : BOOL;
    S_R AT %QX1.1 : BOOL;
    E_R AT %QX1.2 : BOOL;
    W_R AT %QX1.3 : BOOL;
    N_LY AT %QX1.4 : BOOL;
    S_LY AT %QX1.5 : BOOL;
    E_LY AT %QX1.6 : BOOL;
    W_LY AT %QX1.7 : BOOL;
    N_LG AT %QX2.0 : BOOL;
    S_LG AT %QX2.1 : BOOL;
    E_LG AT %QX2.2 : BOOL;
    W_LG AT %QX2.3 : BOOL;
    N_LR AT %QX2.4 : BOOL;
    S_LR AT %QX2.5 : BOOL;
    E_LR AT %QX2.6 : BOOL;
    W_LR AT %QX2.7 : BOOL;
    N_P AT %QX3.0 : BOOL;
    S_P AT %QX3.1 : BOOL;
    E_P AT %QX3.2 : BOOL;
    W_P AT %QX3.3 : BOOL;
    Offset_out AT %QW0 : INT;  (* Outputs to the Field Master *)

    EW_Vehical_Cnt AT %IW0 : INT;   (* Inputs from Sensors *)
    NS_Vehical_Cnt AT %IW1 : INT;   (* Inputs from Sensors *)
    E_Ped_Pressed AT %IX0.0: BOOL;  (* Inputs from Sensors *)
    W_Ped_Pressed AT %IX0.1: BOOL;  (* Inputs from Sensors *)
    N_Ped_Pressed AT %IX0.2: BOOL;  (* Inputs from Sensors *)
    S_Ped_Pressed AT %IX0.3: BOOL;  (* Inputs from Sensors *)
    Offset_in AT %IW2 : INT;             (* Inputs from the Field Master *)
    phase_len_1_in AT %IW3 : INT;        (* Inputs from the Field Master *)
    phase_len_2_in AT %IW4 : INT;
    phase_len_3_in AT %IW5 : INT;
    phase_len_4_in AT %IW6 : INT; 
    phase_len_5_in AT %IW7 : INT;
    phase_len_6_in AT %IW8 : INT;
  END_VAR
  VAR
    pars : Parameter_Array;
    Clear : Clear_States;
    Start_Loop : BOOL := False;
    yellow_in1 : BOOL := False;
    yellow_in2 : BOOL := False;
    yellow_in4 : BOOL := False;
    yellow_in5 : BOOL := False;
    yellow_in6 : BOOL := False;
    Start_Phase_5 : BOOL := False;
    Offset_intv : INT := 15;
    Offset_queue : INT := 0; 
    Phase_1 : Phase_One;
    Phase_2 : Phase_Two;
    Phase_3 : Phase_Three;
    Phase_5 : Phase_Five;
    Phase_6 : Phase_Six;
    TON_Cycle : TON;
    TON_Offset : TON;
    TON_Green_min_1 : TON;
    TON_Green_max_1 : TON;
    TON_Ped_1 : TON;
    TON_Yellow_1 : TON;
    TON_Red_1 : TON;
    Green_real_1 : TIME;
    TON_Green_min_2 : TON;
    TON_Green_max_2 : TON;
    TON_Yellow_2 : TON;
    TON_Red_2 : TON;
    Green_real_2 : TIME;
    TON_Ped_3 : TON;
    TON_Ped_ext_3 : TON;
    TON_Green_min_5 : TON;
    TON_Green_max_5 : TON;
    TON_Yellow_5 : TON;
    TON_Red_5 : TON;
    TON_Ped_5 : TON;
    TON_Green_min_6 : TON;
    TON_Yellow_6 : TON;
    TON_Red_6 : TON;
    TON_Ped_6 : TON;
  END_VAR

  (* Clear the light states *)
  Clear(
     N_G => N_G, N_LG => N_LG, N_Y => N_Y, N_LY => N_LY, N_R => N_R, N_LR => N_LR, N_P => N_P,
     S_G => S_G, S_LG => S_LG, S_Y => S_Y, S_LY => S_LY, S_R => S_R, S_LR => S_LR, S_P => S_P,
     E_G => E_G, E_LG => E_LG, E_Y => E_Y, E_LY => E_LY, E_R => E_R, E_LR => E_LR, E_P => E_P,
     W_G => W_G, W_LG => W_LG, W_Y => W_Y, W_LY => W_LY, W_R => W_R, W_LR => W_LR, W_P => W_P);

  (* Comment out if real inputs are ready *)
  (* Give some test inputs *)
  EW_Vehical_Cnt := 20;
  NS_Vehical_Cnt := 6;
  E_Ped_Pressed := True;
  W_Ped_Pressed := True;
  N_Ped_Pressed := True;
  S_Ped_Pressed := True;
  Offset_in := 35;
  phase_len_1_in := 31;
  phase_len_2_in := 19;
  phase_len_3_in := 0;
  phase_len_4_in := 0; 
  phase_len_5_in := 23; 
  phase_len_6_in := 17;

  (* Adjust the offset at the beginning *)
  (* While adjusting, the red lights at both directions will be on *)
  (* Offset bigger than 15s will be splitted into multiple cycles *)
  Offset_in := MOD(Offset_in, phase_len_1_in + phase_len_2_in + phase_len_3_in + phase_len_4_in + phase_len_5_in + phase_len_6_in);
  Offset_queue := Offset_queue + Offset_in - Offset_out;

  IF (Offset_queue > 0 AND TON_Red_6.Q) THEN
    Offset_queue := Offset_queue - TIME_TO_INT(TON_Offset.PT);
  END_IF;
  IF Offset_queue < 0 THEN
    Offset_queue := 0;
  END_IF;
  IF GT(Offset_queue, Offset_intv) THEN
    TON_Offset(IN := NOT(Start_Loop), PT := INT_TO_TIME(Offset_intv));
  END_IF;
  (* When Offset_in = 0, the TON_Offset.Q can turn True as well *)
  IF (Offset_queue < Offset_intv AND Offset_queue >= 0) THEN
    TON_Offset(IN := NOT(Start_Loop), PT := INT_TO_TIME(Offset_queue));
  END_IF;
  IF (TON_Offset.IN AND NOT(TON_Offset.Q)) THEN
    N_R := True;
    S_R := True;
    E_R := True;
    W_R := True;
  END_IF;
  Offset_out := Offset_in;

  (* --- Start running the Phases --- *)
  (* First Phase: MAX/PED mode*)
  (* Adjust the offset here *)
  (* Array of TON is not supported, so we need to define for each light and phase*)
  (* --- Initilize the Timers ---*)
  TON_Cycle(IN:= TON_Offset.Q, PT:= INT_TO_TIME(phase_len_1_in + phase_len_2_in + phase_len_3_in + phase_len_4_in + phase_len_5_in + phase_len_6_in));
  TON_Green_min_1(IN:= TON_Offset.Q, PT:= pars.min_green_arr[1]); 
  Green_real_1 := INT_TO_TIME(phase_len_1_in) - pars.yellow_cl_arr[1] - pars.red_cl_arr[1];
  TON_Green_max_1(IN:= TON_Offset.Q, PT:= Green_real_1); 
  TON_Ped_1(IN:= TON_Offset.Q, PT:= pars.walk_sec_arr[1]);
  TON_Yellow_1(IN:= yellow_in1, PT:= pars.yellow_cl_arr[1]);
  TON_Red_1(IN:= TON_Yellow_1.Q, PT:= pars.red_cl_arr[1]);
  

  IF TON_Offset.Q THEN
    Phase_1(
      Green_min_1 := TON_Green_min_1.Q,
      Green_max_1 := TON_Green_max_1.Q,
      Veh_cnt := EW_Vehical_Cnt, 
      Ped_1 := TON_Ped_1.Q,
      Ped_Pressed := E_Ped_Pressed,
      Yellow_1 := TON_Yellow_1.Q,
      Red_1 := TON_Red_1.Q,
      W_G => W_G, W_Y => W_Y, W_R => W_R,
      E_G => E_G, E_P => E_P, E_Y => E_Y, E_R => E_R, E_LR => E_LR,
      N_R => N_R, S_R => S_R);
    yellow_in1 := Phase_1.End_of_green;
  END_IF;
 
  (* Second Phase *)
  TON_Green_min_2(IN:= TON_Red_1.Q, PT:= pars.min_green_arr[2]);
  Green_real_2 := INT_TO_TIME(phase_len_2_in) - pars.yellow_cl_arr[2] - pars.red_cl_arr[2]; 
  TON_Green_max_2(IN:= TON_Red_1.Q, PT:= Green_real_2);
  TON_Yellow_2(IN:= yellow_in2, PT:= pars.yellow_cl_arr[2]);
  TON_Red_2(IN:= TON_Yellow_2.Q, PT:= pars.red_cl_arr[2]);
     
  IF AND(TON_Red_1.Q, NOT(TON_Red_2.Q)) THEN
    Phase_2(
      Green_min_2 := TON_Green_min_2.Q,
      Green_max_2 := TON_Green_max_2.Q, 
      Veh_cnt := NS_Vehical_Cnt,    
      Yellow_2 := TON_Yellow_2.Q,
      Red_2 := TON_Red_2.Q,
      N_G => N_G, N_Y => N_Y, N_R => N_R, N_LG => N_LG, N_LY => N_LY,
      S_G => S_G, S_Y => S_Y, S_R => S_R,
      W_R => W_R, E_R => E_R, E_LR => E_LR);
    yellow_in2 := Phase_2.End_of_green;
  END_IF;

  (* Third Phase *)
  TON_Ped_3(IN:= TON_Red_2.Q, PT:= pars.walk_sec_arr[3]);
  TON_Ped_ext_3(IN:= AND(TON_Ped_3.Q, W_Ped_Pressed), PT:= pars.ped_cl_arr[3]);

  IF AND(TON_Red_1.Q, TON_Red_2.Q, OR(NOT(TON_Ped_3.Q), LT(TON_Ped_ext_3.ET, TON_Ped_ext_3.PT))) THEN
    Phase_3(W_P => W_P,
      N_R => N_R,
      S_R => S_R,
      W_R => W_R,
      E_R => E_R,
      E_LR => E_LR);
  END_IF;

  (* Fifth Phase *)
  Start_Phase_5 := AND(TON_Ped_3.Q, NOT(XOR(TON_Ped_ext_3.Q, W_Ped_Pressed)));
  TON_Green_min_5(IN:= Start_Phase_5, PT:= pars.min_green_arr[5]);
  TON_Green_max_5(IN:= Start_Phase_5, PT:= pars.max_green_arr[5]);
  TON_Ped_5(IN:= Start_Phase_5, PT:= pars.walk_sec_arr[5]);
  TON_Yellow_5(IN:= yellow_in5, PT:= pars.yellow_cl_arr[5]);
  TON_Red_5(IN:= TON_Yellow_5.Q, PT:= pars.red_cl_arr[5]);

  IF AND(TON_Red_1.Q, TON_Red_2.Q, Start_Phase_5, NOT(TON_Red_5.Q)) THEN
    Phase_5(
      Green_min_5 := TON_Green_min_5.Q,
      Green_max_5 := TON_Green_max_5.Q,
      Yellow_5 := TON_Yellow_5.Q,
      Red_5 := TON_Red_5.Q,
      Ped_5 := TON_Ped_5.Q,
      Ped_Pressed := S_Ped_Pressed,
      End_Cycle := TON_Cycle.PT - (pars.min_green_arr[6] + pars.yellow_cl_arr[6] + pars.red_cl_arr[6]) - TON_Cycle.ET,
      N_G => N_G, N_Y => N_Y, N_R => N_R,
      S_G => S_G, S_Y => S_Y, S_R => S_R, S_P => S_P,
      W_R => W_R, 
      E_R => E_R, E_LR => E_LR);
    yellow_in5 := Phase_5.End_of_Green;
  END_IF;

  (* Six Phase*)
  TON_Green_min_6(IN:= TON_Red_5.Q, PT:= pars.min_green_arr[6]);
  TON_Ped_6(IN:= TON_Red_5.Q, PT:= pars.walk_sec_arr[5]);
  TON_Yellow_6(IN:= yellow_in6, PT:= pars.yellow_cl_arr[6]);
  TON_Red_6(IN:= TON_Yellow_6.Q, PT:= pars.red_cl_arr[6]);

  IF AND(TON_Red_5.Q, NOT(TON_Red_6.Q)) THEN
    Phase_6(
      Green_6 := TON_Green_min_6.Q,
      Ped_6 := TON_Ped_6.Q,
      Yellow_6 := TON_Yellow_6.Q,
      Red_6 := TON_Red_6.Q,
      Ped_Pressed := N_Ped_Pressed,
      End_Cycle := TON_Cycle.PT - TON_Cycle.ET,
      E_G => E_G, E_LG => E_LG, E_Y => E_Y, E_LY => E_LY,
      E_R => E_R, E_LR => E_LR, N_P => N_P,
      W_R => W_R, N_R => N_R, S_R => S_R);
    yellow_in6 := Phase_6.End_of_Green;
  END_IF;

  Start_Loop := TON_Red_6.Q; 
  IF Start_Loop THEN
    yellow_in1 := False;
    yellow_in2 := False;
    yellow_in5 := False;
    yellow_in6 := False;
  END_IF;

END_PROGRAM


CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#100ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : Ruggles_Street;
  END_RESOURCE
END_CONFIGURATION
