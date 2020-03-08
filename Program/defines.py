side_ratio = 16 / 9
initial_height = 600
initial_width = initial_height * side_ratio

reduced_price_flag = "R"
normal_price_flag = "N"

reduced_price_value = 0.3
normal_price_value = 0.5
initial_debounce = 0

active_user_flag = "A"
inactive_user_flag = "I"

PayPal = "P"
Bar = "B"
Material = "M"
Serivce = "S"
Unknown = "U"

gui_title = '(G)ui (B)ased (C)haring (T)erminal - GBCT'

initial_number_value = "0.00"
default_str_nr = "-1"
no_card_found_state = "0"
card_found_state = "1"
no_text = ""

debug = True

German = "D"
English = "E"

language = German

paypal_label = "PayPal"
material_label = "Material"
service_label = "Service"

name_label = "Name"
upload_button_txt = "Update Chip"

price_sql_txt = 'price'
status_sql_txt = 'status'

new_user_flag = "NU"
edit_user_flag = "EU"

if language == German:
    cash_label = "Bar"
    service_payment_information = "Justierung"
    no_old_ids_txt = "Keine alten ID's gefunden"
    no_deposits_txt = "Keine Einzahlungen gefunden"
    user_id_history_tab_name = "ID Historie"
    user_deposits_tab_name = "Einzahlungen"
    user_selector_active_name = "Aktive Benutzer"
    user_selector_inactive_name = "Inaktive Benutzer"
    actual_id_label = "Aktuelle ID"
    reduced_price_label = "Reduzierter Preis"
    active_user_label = "Aktiver Nutzer"
    edit_label = "Bearbeiten"
    new_user_label = "Neuer Butzer"
    total_deposit_label = "Gesamteinzahlung in €"
    total_consumption_label = "Gesamtverbrauch (Schätzung)"
    connect_label = "Verbinden"
    amount_label_txt = "Eingezahlter Betrag"
    old_amount_label_txt = "Aktuelles Guthaben"
    new_amount_label_txt = "Neues Guthaben"
    reset_button_txt = "Initialisier Chip"
    deposit_type_label_txt = "Art der Einzahlung"
    safe_label_txt = "Speichern"
    checking = "Prüfe"
    service_amound_txt = "Service Guthaben"
    unknown_id_msg_box_title = "Unbekannte ID"
    unknow_id_msg_box_text = "Unbekannte ID - {ID}"
    new_user_label = "Neuer Nutzer anlegen"
    edit_user_label = "Zugehörige ID bearbeiten"
    back_label = "Zurück"
    given_name = "Vorname"
    surname = "Nachname"
    Cancel_lable = "Abruch"
    delete_lable = "Löschen"
    delete_question_txt = "{name} wirklich löschen?\nDieser Vorgang kann nicht rückgänig gemacht werden."
    add_user_lable = "Benutzer hinzufügen"
    add_id_lable = "ID hinzufügen"
    new_user_list_label = "Rechtsklick für neuen Nutzer"
    new_ID_list_label = "Rechtsklick für neue ID"
    edit_from_signal_txt = "Nutzer wähen..."
    needs_to_be_edited_label = "Unbekannt"


else:
    cash_label = "Cash"
    service_payment_information = "Adjustment"
    no_old_ids_txt = "No old ID's found"
    no_deposits_txt = "No deposits found"
    user_id_history_tab_name = "ID History"
    user_deposits_tab_name = "Deposits"
    user_selector_active_name = "Active User"
    user_selector_inactive_name = "Inactive User"
    actual_id_label = "Current ID"
    reduced_price_label = "Reduced price"
    active_user_label = "Active user"
    edit_label = "Edit"
    new_user_label = "New user"
    total_deposit_label = "Total deposit in €"
    total_consumption_label = "Total consumption (estimation)"
    connect_label = "Connect"
    amount_label_txt = "Paid deposit"
    old_amount_label_txt = "Current deposit"
    new_amount_label_txt = "New deposit"
    reset_button_txt = "Initialize Chip"
    deposit_type_label_txt = "Type of deposit"
    safe_label_txt = "Safe"
    checking = "Checking"
    service_amound_txt = "Service deposit"
    unknown_id_msg_box_title = " ID"
    unknow_id_msg_box_text = "A unknown ID - {ID}"
    new_user_label = "Add new user"
    edit_user_label = "Edit user ID"
    back_label = "Back"
    given_name = "Given name"
    surname = "Surname"
    Cancel_lable = "Cancel"
    delete_lable = "Delete"
    delete_question_txt = "Do you realy want to delete {name}?\nYou can't undo that."
    add_user_lable = "Add user"
    add_id_lable = "Add ID"
    new_user_list_label = "Right click for new user"
    new_ID_list_label = "Right click for new ID"
    edit_from_signal_txt = "Choose user..."
    needs_to_be_edited_label = "Unknown"










