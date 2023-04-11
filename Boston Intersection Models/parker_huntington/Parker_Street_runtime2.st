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
    W_P : BOOL;
    E_P : BOOL;
    W_Y : BOOL;
    E_Y : BOOL;
    W_R : BOOL;
    E_R : BOOL;
    N_R : BOOL;
    S_R : BOOL;
    End_of_green : BOOL := False;
  END_VAR
  VAR
    vehical_ext_arr : ARRAY [1..3] OF TIME := [T#2s, T#3s, T#2s];
    red_cl_arr : ARRAY [1..3] OF TIME := [T#3s, T#4s, T#5s];
    ped_cl_arr : ARRAY [1..3] OF TIME := [T#23s, T#7s, T#0s];
    veh_total : INT;
    veh_total_prev : INT;
    TON_Veh_ext : TON;
    TON_Ped_ext : TON;
    start_veh_TON : BOOL := False;
    start_ped_TON : BOOL := False;
  END_VAR

  start_veh_TON := Red_1;
  start_ped_TON := Red_1;

  (* vehical extends green: MAX mode *)
  veh_total := MUL(Veh_cnt, TIME_TO_INT(vehical_ext_arr[1])); 
  IF veh_total > veh_total_prev THEN
    TON_Veh_ext(IN := AND(NOT(start_veh_TON), Green_min_1), PT := INT_TO_TIME(veh_total - veh_total_prev));
  END_IF;
  veh_total_prev := veh_total;

  (* Pedestrian clearance only happens when green is not ended, and ped button is pressed *)
  (* Ped clearance can extend to the end of yellow ON *)
  TON_Ped_ext(IN := AND(NOT(start_ped_TON), Ped_1, Ped_Pressed), PT := ped_cl_arr[1]);

  End_of_green := AND(Green_min_1, OR(TON_Veh_ext.Q, Green_max_1)); 

  W_G := AND(NOT(End_of_green));
  E_G := AND(NOT(End_of_green));
  W_P := AND(OR(NOT(Ped_1), AND(TON_Ped_ext.IN, NOT(TON_Ped_ext.Q))), NOT(Yellow_1));
  E_P := W_P;
  W_Y := AND(End_of_green, NOT(Yellow_1));
  E_Y := AND(End_of_green, NOT(Yellow_1));
  W_R := AND(Yellow_1, NOT(Red_1));
  E_R := AND(Yellow_1, NOT(Red_1));
  N_R := True;
  S_R := True;

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
    N_P : BOOL;
    S_P : BOOL;
    N_Y : BOOL;
    S_Y : BOOL;
    N_R : BOOL;
    S_R : BOOL;
    W_R : BOOL;
    E_R : BOOL;
    End_of_green : BOOL := False;
  END_VAR
  VAR
    min_green_arr : ARRAY [1..3] OF TIME := [T#8s, T#8s, T#6s];
    max_green_arr : ARRAY [1..3] OF TIME := [T#32s, T#37s, T#16s];
    vehical_ext_arr : ARRAY [1..3] OF TIME := [T#2s, T#3s, T#2s];
    yellow_cl_arr : ARRAY [1..3] OF TIME := [T#3s500ms, T#3s500ms, T#3s];
    red_cl_arr : ARRAY [1..3] OF TIME := [T#3s, T#4s, T#5s];
    walk_sec_arr : ARRAY [1..3] OF TIME := [T#7s, T#7s, T#0s];
    ped_cl_arr : ARRAY [1..3] OF TIME := [T#23s, T#7s, T#0s];
    phase_len_arr : ARRAY [1..3] OF TIME := [T#38s, T#34s, T#18s];
    veh_total : INT;
    veh_total_prev : INT;
    TON_Veh_ext : TON;
    TON_Ped_ext : TON;
    start_veh_TON : BOOL := False;
    start_ped_TON : BOOL := False;
  END_VAR

  start_veh_TON := Red_2;
  start_ped_TON := Red_2;
  
  (* Second Phase*)
  veh_total := MUL(Veh_cnt, TIME_TO_INT(vehical_ext_arr[2]));   
  IF veh_total > veh_total_prev THEN
    TON_Veh_ext(IN := AND(NOT(start_veh_TON), Green_min_2), PT := INT_TO_TIME(veh_total - veh_total_prev));
  END_IF;
  veh_total_prev := veh_total;

  TON_Ped_ext(IN := AND(NOT(start_ped_TON), Ped_2, Ped_Pressed), PT := ped_cl_arr[2]);

  End_of_green := AND(Green_min_2, OR(TON_Veh_ext.Q, Green_max_2)); 

  N_G := NOT(End_of_green);
  S_G := NOT(End_of_green);
  N_P := AND(OR(NOT(Ped_2), AND(TON_Ped_ext.IN, NOT(TON_Ped_ext.Q))), NOT(Yellow_2));
  S_P := N_P;
  N_Y := AND(End_of_green, NOT(Yellow_2));
  S_Y := AND(End_of_green, NOT(Yellow_2));
  N_R := AND(Yellow_2, NOT(Red_2));
  S_R := AND(Yellow_2, NOT(Red_2));
  W_R := True;
  E_R := True;

END_FUNCTION_BLOCK


FUNCTION_BLOCK Phase_Three
  VAR_INPUT
    Red_3 : BOOL;
    Green_3 : BOOL;
    Yellow_3 : BOOL;
    End_Cycle : TIME;
  END_VAR
  VAR_OUTPUT
    W_G : BOOL;
    W_LG : BOOL;
    W_Y : BOOL;
    W_LY : BOOL;
    W_R : BOOL;
    W_LR : BOOL;
    N_R : BOOL;
    S_R : BOOL;
    E_R : BOOL;
    End_of_Green : BOOL := False;
  END_VAR
  VAR
    min_green_arr : ARRAY [1..3] OF TIME := [T#8s, T#8s, T#6s];
    max_green_arr : ARRAY [1..3] OF TIME := [T#32s, T#37s, T#16s];
    vehical_ext_arr : ARRAY [1..3] OF TIME := [T#2s, T#3s, T#2s];
    yellow_cl_arr : ARRAY [1..3] OF TIME := [T#3s500ms, T#3s500ms, T#3s];
    red_cl_arr : ARRAY [1..3] OF TIME := [T#3s, T#4s, T#5s];
    walk_sec_arr : ARRAY [1..3] OF TIME := [T#7s, T#7s, T#0s];
    ped_cl_arr : ARRAY [1..3] OF TIME := [T#23s, T#7s, T#0s];
    phase_len_arr : ARRAY [1..3] OF TIME := [T#38s, T#34s, T#18s];
  END_VAR

  (* Third Phase*)
  End_of_Green := False;

  IF LE(End_Cycle, yellow_cl_arr[3] + red_cl_arr[3]) THEN
    End_of_Green := True;
  END_IF;

  W_G := NOT(End_of_Green);
  W_LG := NOT(End_of_Green);

  W_Y := AND(End_of_Green, NOT(Yellow_3));
  W_LY := AND(End_of_Green, NOT(Yellow_3));

  W_R := AND(Yellow_3, NOT(Red_3));
  W_LR := AND(Yellow_3, NOT(Red_3));

  E_R := True;
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

PROGRAM Parker_Street
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
    Offset_out AT %QW0 : INT := 0;   (* Outputs to the Field Master *)

    EW_Vehical_Cnt AT %IW0 : INT;   (* Inputs from Sensors *)
    NS_Vehical_Cnt AT %IW1 : INT;   (* Inputs from Sensors *)
    EW_Ped_Pressed AT %IX0.0: BOOL; (* Inputs from Sensors *)
    NS_Ped_Pressed AT %IX0.1: BOOL; (* Inputs from Sensors *)
    Offset_in AT %IW2 : INT;             (* Inputs from the Field Master *)
    phase_len_1_in AT %IW3 : INT;        (* Inputs from the Field Master *)
    phase_len_2_in AT %IW4 : INT;        (* Inputs from the Field Master *)
    phase_len_3_in AT %IW5 : INT;        (* Inputs from the Field Master *)
  END_VAR
  VAR
    Start_Loop : BOOL := False;
    TON_Cycle : TON;
    TON_Yellow_1 : TON;
    TON_Yellow_2 : TON;
    TON_Yellow_3 : TON;
    TON_Ped_1 : TON;
    TON_Ped_2 : TON;
    TON_Red_1 : TON;
    TON_Red_2 : TON;
    TON_Red_3 : TON;
    TON_Green_min_1 : TON;
    TON_Green_max_1 : TON;
    TON_Green_min_2 : TON;
    TON_Green_max_2 : TON;
    TON_Green_max_3 : TON;
    TON_Offset : TON;

    min_green_arr : ARRAY [1..3] OF TIME := [T#8s, T#8s, T#6s];
    max_green_arr : ARRAY [1..3] OF TIME := [T#32s, T#37s, T#16s];
    vehical_ext_arr : ARRAY [1..3] OF TIME := [T#2s, T#3s, T#2s];
    yellow_cl_arr : ARRAY [1..3] OF TIME := [T#3s500ms, T#3s500ms, T#3s];
    red_cl_arr : ARRAY [1..3] OF TIME := [T#3s, T#4s, T#5s];
    walk_sec_arr : ARRAY [1..3] OF TIME := [T#7s, T#7s, T#0s];
    ped_cl_arr : ARRAY [1..3] OF TIME := [T#23s, T#7s, T#0s];
    phase_len_arr : ARRAY [1..3] OF TIME := [T#38s, T#34s, T#18s];

    Clear : Clear_States;
    Phase_1 : Phase_One;
    Phase_2 : Phase_Two;
    Phase_3 : Phase_Three;
    Green_real_2 : TIME; (* This is the real max green for Phase 2 *)
    Offset_intv : INT := 15;
    Offset_queue : INT := 0; 
    yellow_in1 : BOOL := False;
    yellow_in2 : BOOL := False;
    yellow_in3 : BOOL := False;
  END_VAR

  (* Clear the light states*)
  Clear(
       N_G => N_G, N_LG => N_LG, N_Y => N_Y, N_LY => N_LY, N_R => N_R, N_LR => N_LR, N_P => N_P,
       S_G => S_G, S_LG => S_LG, S_Y => S_Y, S_LY => S_LY, S_R => S_R, S_LR => S_LR, S_P => S_P,
       E_G => E_G, E_LG => E_LG, E_Y => E_Y, E_LY => E_LY, E_R => E_R, E_LR => E_LR, E_P => E_P,
       W_G => W_G, W_LG => W_LG, W_Y => W_Y, W_LY => W_LY, W_R => W_R, W_LR => W_LR, W_P => W_P);

  (* Comment out if real inputs are ready *)
  (* Give some test inputs *)
  EW_Vehical_Cnt := 20;
  NS_Vehical_Cnt := 6;
  EW_Ped_Pressed := True;
  NS_Ped_Pressed := True;
  Offset_in := 35;            
  phase_len_1_in := 38;       
  phase_len_2_in := 34;       
  phase_len_3_in := 18;       


  (* Adjust the offset at the beginning *)
  (* While adjusting, the red lights at both directions will be on *)
  (* Offset bigger than 15s will be splitted into multiple cycles *)

  Offset_in := MOD(Offset_in, phase_len_1_in + phase_len_2_in + phase_len_3_in);
  Offset_queue := Offset_queue + Offset_in - Offset_out;

  IF (Offset_queue > 0 AND TON_Red_3.Q) THEN
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
  (* First Phase*)
  (* Adjust the offset here *)
  (* Array of TON is not supported, so we need to define for each light and phase*)
  (* --- Initilize the Timers ---*)
  TON_Cycle(IN:= TON_Offset.Q, PT:= INT_TO_TIME(phase_len_1_in + phase_len_2_in + phase_len_3_in));
  TON_Green_min_1(IN:= TON_Offset.Q, PT:= min_green_arr[1]); 
  TON_Green_max_1(IN:= TON_Offset.Q, PT:= max_green_arr[1]); 
  TON_Ped_1(IN:= TON_Offset.Q, PT:= walk_sec_arr[1]);
  TON_Yellow_1(IN:= yellow_in1, PT:= yellow_cl_arr[1]);
  TON_Red_1(IN:= TON_Yellow_1.Q, PT:= red_cl_arr[1]);
  
  IF TON_Offset.Q THEN
    Phase_1(
      Green_min_1 := TON_Green_min_1.Q,
      Green_max_1 := TON_Green_max_1.Q,
      Veh_cnt := EW_Vehical_Cnt, 
      Ped_1 := TON_Ped_1.Q,
      Ped_Pressed := EW_Ped_Pressed,
      Yellow_1 := TON_Yellow_1.Q,
      Red_1 := TON_Red_1.Q,
      W_G => W_G, W_P => W_P, W_Y => W_Y, W_R => W_R,
      E_G => E_G, E_P => E_P, E_Y => E_Y, E_R => E_R,
      N_R => N_R, S_R => S_R);
    yellow_in1 := Phase_1.End_of_green;
  END_IF;


  (* Second Phase*)
  TON_Green_min_2(IN:= TON_Red_1.Q, PT:= min_green_arr[2]);
  Green_real_2 := INT_TO_TIME(phase_len_2_in) - yellow_cl_arr[2] - red_cl_arr[2]; 
  TON_Green_max_2(IN:= TON_Red_1.Q, PT:= Green_real_2);
  TON_Yellow_2(IN:= yellow_in2, PT:= yellow_cl_arr[2]);
  TON_Ped_2(IN:= TON_Red_1.Q, PT:= walk_sec_arr[2]);
  TON_Red_2(IN:= TON_Yellow_2.Q, PT:= red_cl_arr[2]);

  IF AND(TON_Red_1.Q, NOT(TON_Red_2.Q)) THEN
    Phase_2(
      Green_min_2 := TON_Green_min_2.Q,
      Green_max_2 := TON_Green_max_2.Q, 
      Veh_cnt := NS_Vehical_Cnt,    
      Ped_2 := TON_Ped_2.Q,
      Ped_Pressed := NS_Ped_Pressed,
      Yellow_2 := TON_Yellow_2.Q,
      Red_2 := TON_Red_2.Q,
      N_G => N_G, N_P => N_P, N_Y => N_Y, N_R => N_R,
      S_G => S_G, S_P => S_P, S_Y => S_Y, S_R => S_R,
      W_R => W_R, E_R => E_R);
    yellow_in2 := Phase_2.End_of_green;
  END_IF;


  (* Third Phase*)
  TON_Green_max_3(IN:= TON_Red_2.Q, PT:= max_green_arr[3]);
  TON_Yellow_3(IN:= yellow_in3, PT:= yellow_cl_arr[3]);
  TON_Red_3(IN:= TON_Yellow_3.Q, PT:= red_cl_arr[3]);

  IF AND(TON_Red_1.Q, TON_Red_2.Q, NOT(TON_Red_3.Q)) THEN
    Phase_3(
      Green_3 := TON_Green_max_3.Q,
      Yellow_3 := TON_Yellow_3.Q,
      End_Cycle := TON_Cycle.PT - TON_Cycle.ET,
      Red_3 := TON_Red_3.Q,
      W_G => W_G, W_LG => W_LG, W_Y => W_Y, W_LY => W_LY,
      W_R => W_R, W_LR => W_LR, 
      E_R => E_R, N_R => N_R, S_R => S_R);
    yellow_in3 := Phase_3.End_of_Green;
  END_IF;

  Start_Loop := TON_Red_3.Q; 
  IF Start_Loop THEN
    yellow_in1 := False;
    yellow_in2 := False;
    yellow_in3 := False;
  END_IF;

END_PROGRAM


CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#100ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : Parker_Street;
  END_RESOURCE
END_CONFIGURATION
