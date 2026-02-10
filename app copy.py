# """
# Net Calorie Tracker - Main Streamlit Application
# STEP 0: Empty skeleton - just verify Streamlit runs
# """

# import streamlit as st
# import datetime
# import pandas as pd
# from services.user_service import create_user, get_all_users, delete_user
# from services.bmr_service import calculate_bmr
# from services.calorie_service import get_all_foods, get_daily_log, save_daily_log
# from models.user_model import User
# from models.log_model import DailyLog, FoodEntry
# from utils.date_utils import format_date_for_db
# from pymongo.errors import ServerSelectionTimeoutError

# st.set_page_config(page_title="Net Calorie Tracker", page_icon="🍎", layout="wide")

# # Global error handling and UI Helpers
# def handle_db_error(e):
#     st.error("Database Connection Error! Please make sure MongoDB is running.")
#     st.info("Check your `.env` file and ensure `localhost:27017` is accessible.")
#     st.stop()

# def render_selection_logic(items, cat_field, item_field, cat_label, item_label, key_prefix):
#     """Handles the cascading Select Group -> Select Item logic for both Food and Activities."""
#     unique_cats = sorted(list(set(str(getattr(i, cat_field)) for i in items if getattr(i, cat_field))))
    
#     col1, col2 = st.columns(2)
#     cat_opts = [f"-- Select {cat_label} --", "Manual Entry"] + unique_cats
#     sel_cat = col1.selectbox(cat_label, cat_opts, key=f"{key_prefix}_cat")
    
#     if sel_cat not in [f"-- Select {cat_label} --", "Manual Entry"]:
#         filtered = sorted(list(set(str(getattr(i, item_field)) for i in items if str(getattr(i, cat_field)) == sel_cat and getattr(i, item_field))))
#     else:
#         filtered = sorted(list(set(str(getattr(i, item_field)) for i in items if getattr(i, item_field))))
        
#     item_opts = [f"-- Select {item_label} --", "Manual Entry"] + filtered
#     sel_item = col2.selectbox(item_label, item_opts, key=f"{key_prefix}_item")
    
#     return sel_cat, sel_item

# def resolve_item_details(items, sel_cat, sel_item, cat_field, item_field, cat_label, item_label):
#     """Resolves the database object based on dropdown selections."""
#     if sel_item not in [f"-- Select {item_label} --", "Manual Entry"]:
#         if sel_cat not in [f"-- Select {cat_label} --", "Manual Entry"]:
#             return next((i for i in items if str(getattr(i, cat_field)) == sel_cat and str(getattr(i, item_field)) == sel_item), None)
#         return next((i for i in items if str(getattr(i, item_field)) == sel_item), None)
#     return None

# # Navigation Sidebar
# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to", ["User Management", "Calorie Tracker"])

# if page == "User Management":
#     st.title("👤 User Management")
    
#     # Form to add a new user
#     with st.expander("Add New User", expanded=True):
#         with st.form("add_user_form", clear_on_submit=True):
#             col1, col2 = st.columns(2)
#             with col1:
#                 name = st.text_input("Name")
#                 age = st.number_input("Age", min_value=1, max_value=120, value=25)
#                 sex = st.selectbox("Sex", ["Male", "Female"])
#             with col2:
#                 weight = st.number_input("Weight (kg)", min_value=1.0, value=70.0)
#                 height = st.number_input("Height (cm)", min_value=1.0, value=170.0)
            
#             submit = st.form_submit_button("Add User")
            
#             if submit:
#                 if name:
#                     try:
#                         new_user = User(name=name, weight=weight, height=height, sex=sex, age=age)
#                         user_id = create_user(new_user)
#                         st.success(f"User {name} added successfully!")
#                         st.rerun()
#                     except Exception as e:
#                         handle_db_error(e)
#                 else:
#                     st.error("Please enter a name.")

#     # List users
#     st.subheader("Existing Users")
#     try:
#         users = get_all_users()
#     except Exception as e:
#         handle_db_error(e)
    
#     if not users:
#         st.info("No users found. Please add a user above.")
#     else:
#         # Create a table/display for users
#         for user in users:
#             col_info, col_delete = st.columns([4, 1])
#             with col_info:
#                 st.write(f"**{user.name}** - {user.sex}, {user.age} years, {user.weight}kg, {user.height}cm")
#             with col_delete:
#                 if st.button("Delete", key=f"del_{user._id}"):
#                     try:
#                         if delete_user(user._id):
#                             st.success(f"User deleted.")
#                             st.rerun()
#                         else:
#                             st.error("Failed to delete user.")
#                     except Exception as e:
#                         handle_db_error(e)
#             st.divider()

# else:
#     try:
#         users = get_all_users()
#     except Exception as e:
#         handle_db_error(e)

#     if not users:
#         st.title("Calories Tracker")
#         st.warning("No users found. Please create a user in 'User Management' first.")
#     else:
#         # User selection first to determine the title
#         user_names = [u.name for u in users]
#         selected_user_name = st.selectbox("Select User Profile", user_names)
        
#         # Dynamic Title with Name
#         st.title(f"Calories Tracker - {selected_user_name}")

#         from services.calorie_service import get_all_foods, get_daily_log, save_daily_log, get_all_activities, delete_daily_log, delete_food_entry, delete_activity_entry
#         from models.log_model import DailyLog, FoodEntry, ActivityEntry
#         selected_user = next(u for u in users if u.name == selected_user_name)
        
#         # Date Selection
#         today = datetime.date.today()
#         min_date = today - datetime.timedelta(days=30)
#         selected_date = st.date_input("Select Date", value=today, min_value=min_date, max_value=today)
#         date_str = format_date_for_db(selected_date)

#         try:
#             daily_log = get_daily_log(selected_user._id, date_str)
#             foods = get_all_foods()
#             activities = get_all_activities()
#         except Exception as e:
#             handle_db_error(e)

#         if not daily_log:
#             # Calculate BMR once for the day
#             bmr = calculate_bmr(selected_user.weight, selected_user.height, selected_user.age, selected_user.sex)
#             daily_log = DailyLog(user_id=selected_user._id, date=date_str, bmr_at_time=bmr)

#         # Dashboard Header with Clear Button
#         st.divider()
#         col_title, col_reset = st.columns([4, 1])
#         with col_title:
#             st.subheader(f" Daily Energy Balance for {selected_user.name}")
#         with col_reset:
#             if st.button("Clear Day", help="Delete all logs for this date"):
#                 try:
#                     if delete_daily_log(selected_user._id, date_str):
#                         st.success("Day cleared successfully!")
#                         st.rerun()
#                     else:
#                         st.info("No logs found to clear.")
#                 except Exception as e:
#                     handle_db_error(e)
        
#         total_calories_in = sum(f.calories for f in daily_log.foods)
#         total_calories_out = sum(a.calories_burnt for a in daily_log.activities)
#         net_calories = total_calories_in - daily_log.bmr_at_time - total_calories_out
        
#         col_bmr, col_in, col_out, col_net = st.columns(4)
        
#         col_in.metric(" Calories IN (Food)", f"{total_calories_in:.0f} kcal")
#         col_bmr.metric("BMR (Base Burn)", f"{daily_log.bmr_at_time:.0f} kcal")
#         col_out.metric("Activity Burn", f"{total_calories_out:.0f} kcal")
        
#         # Net calories logic: Positive means surplus, Negative means deficit
#         net_label = "Surplus" if net_calories > 0 else "Deficit"
#         col_net.metric(
#             f"Net ({net_label})", 
#             f"{net_calories:.0f} kcal", 
#             delta=f"{net_calories:.0f} vs Baseline",
#             delta_color="inverse" # Red for surplus (usually), Green for deficit
#         )

#         # Formula helper
#         st.caption(f"**Formula**: {total_calories_in:.0f} (Food) - {daily_log.bmr_at_time:.0f} (BMR) - {total_calories_out:.0f} (Exercise) = **{net_calories:.0f} kcal**")
        
#         if net_calories < 0:
#             st.success(f" You are in a **deficit** of {abs(net_calories):.0f} kcal today. Great for weight loss!")
#         elif net_calories > 0:
#             st.warning(f" You have a **surplus** of {net_calories:.0f} kcal today.")
#         else:
#             st.info(" You are exactly at maintenance calories today.")

#         # --- Daily Macro Summary Section ---
#         total_p = sum(f.protein for f in daily_log.foods)
#         total_f = sum(f.fat for f in daily_log.foods)
#         total_c = sum(f.carbs for f in daily_log.foods)

#         st.subheader(" Daily Macro Totals")
#         m1, m2, m3 = st.columns(3)
#         m1.metric("Total Protein", f"{total_p:.1f}g")
#         m2.metric("Total Fat", f"{total_f:.1f}g")
#         m3.metric("Total Carbohydrates", f"{total_c:.1f}g")

#         st.divider()

#         # Input Layout: Food and Activity in Tabs for better space management
#         st.subheader("Daily Logging")
#         tab_food, tab_act = st.tabs(["Add Food Intake", "Add Activity"])

#         with tab_food:
#             # --- Categorized Selection ---
#             st.markdown("---")
#             st.markdown("**Categorized Selection**")
            
#             f_cat, f_name = render_selection_logic(foods, "food_group", "food_name", "Category", "Food", "food")

#             # --- Form for Details & Submission ---
#             with st.form("food_entry_form_unified", clear_on_submit=True):
#                 st.markdown("**Entry Details**")
                
#                 active_food = resolve_item_details(foods, f_cat, f_name, "food_group", "food_name", "Category", "Food")

#                 # Resolved defaults for fields below
#                 res_name = active_food.food_name if active_food else ""
#                 res_group = active_food.food_group if active_food else ""
#                 res_cals = float(active_food.calories_per_serving) if active_food else 0.0
#                 res_p = float(active_food.protein) if active_food else 0.0
#                 res_f = float(active_food.fat) if active_food else 0.0
#                 res_c = float(active_food.carbs) if active_food else 0.0

#                 col_m_name, col_m_group = st.columns(2)
#                 custom_name = col_m_name.text_input("Name", value=res_name, placeholder="Confirm/Edit Food Name")
#                 custom_group = col_m_group.text_input("Group", value=str(res_group), placeholder="Confirm/Edit Group")

#                 col_c1, col_c2, col_meal = st.columns([1, 1, 1])
#                 f_cals = col_c1.number_input("Calories (per serving)", min_value=0.0, value=res_cals)
#                 f_portion = col_c2.number_input("Portion / Multiplier", min_value=0.1, value=1.0, step=0.1)
#                 f_meal = col_meal.selectbox("Meal Period", ["Breakfast", "Lunch", "Dinner", "Snack"])
                
#                 st.markdown("##### Macros (Optional)")
#                 mc1, mc2, mc3 = st.columns(3)
#                 f_p = mc1.number_input("Protein (g)", min_value=0.0, value=res_p)
#                 f_f = mc2.number_input("Fat (g)", min_value=0.0, value=res_f)
#                 f_c = mc3.number_input("Carbohydrates (g)", min_value=0.0, value=res_c)
                
#                 add_food = st.form_submit_button("Log Food Intake")
                
#                 if add_food:
#                     final_f_name = custom_name
#                     final_f_group = custom_group
                    
#                     if not final_f_name:
#                         st.error("Please enter a food name.")
#                     else:
#                         try:
#                             # Final resolution for database tracking
#                             match = next((f for f in foods if str(f.food_name) == final_f_name and str(f.food_group) == final_f_group), None)
                            
#                             food_id = str(match._id) if match else "manual"
#                             excel_id = match.excel_id if match else None
#                             serving_desc = match.serving_size if match else "1 serving"

#                             final_total_cals = f_cals * f_portion
                            
#                             new_entry = FoodEntry(
#                                 food_id=food_id,
#                                 food_name=final_f_name,
#                                 portion=f_portion,
#                                 calories=final_total_cals,
#                                 meal_type=f_meal,
#                                 fat=f_f * f_portion,
#                                 protein=f_p * f_portion,
#                                 carbs=f_c * f_portion,
#                                 excel_id=excel_id,
#                                 food_group=final_f_group,
#                                 serving_desc=serving_desc
#                             )
                            
#                             daily_log.foods.append(new_entry)
#                             daily_log.net_calories = total_calories_in + final_total_cals - daily_log.bmr_at_time - total_calories_out
#                             save_daily_log(daily_log)
#                             st.success(f"Logged {final_f_name}")
#                             st.rerun()
#                         except Exception as e:
#                             handle_db_error(e)

#         with tab_act:
#             # --- Categorized Selection ---
#             st.markdown("---")
#             st.markdown("**Activity Selection**")
            
#             a_cat, a_mot = render_selection_logic(activities, "activity_name", "specific_motion", "List", "Motion List", "act")

#             # --- Form for Details & Submission ---
#             with st.form("act_entry_form_unified_final_reactive", clear_on_submit=True):
#                 st.markdown("**Activity Details**")
                
#                 matched_act = resolve_item_details(activities, a_cat, a_mot, "activity_name", "specific_motion", "List", "Motion List")
                
#                 # Resolved defaults for fields below
#                 res_a_name = matched_act.activity_name if matched_act else ""
#                 res_motion = matched_act.specific_motion if matched_act else ""
#                 res_met = float(matched_act.met_value) if matched_act else 0.0

#                 col_name_man, col_mot_man = st.columns(2)
#                 final_a_name = col_name_man.text_input("Activity Name", value=res_a_name, placeholder="Confirm/Edit Activity")
#                 final_a_motion = col_mot_man.text_input("Manual/Custom Name", value=res_motion, placeholder="Confirm/Edit Motion")
                
#                 col_dur, col_burn = st.columns(2)
#                 f_dur = col_dur.number_input("Duration (minutes)", min_value=1.0, value=30.0)
                
#                 # Calculate default burn
#                 default_burnt = res_met * selected_user.weight * (f_dur / 60)

#                 f_burnt = col_burn.number_input("Calories Burnt (Total)", min_value=0.0, value=default_burnt, help="Calculated automatically for DB items.")
                
#                 add_act = st.form_submit_button("Log Activity")
                
#                 if add_act:
#                     if not final_a_name:
#                         st.error("Please enter an activity name.")
#                     else:
#                         try:
#                             # Resolve activity ID
#                             activity_id = str(matched_act._id) if matched_act else "manual"
                            
#                             new_entry = ActivityEntry(
#                                 activity_id=activity_id,
#                                 activity_name=final_a_name,
#                                 duration_minutes=f_dur,
#                                 calories_burnt=f_burnt,
#                                 specific_motion=final_a_motion
#                             )
#                             daily_log.activities.append(new_entry)
#                             daily_log.net_calories = total_calories_in - daily_log.bmr_at_time - (total_calories_out + f_burnt)
#                             save_daily_log(daily_log)
#                             st.success(f"Logged {final_a_name}")
#                             st.rerun()
#                         except Exception as e:
#                             handle_db_error(e)

#         # Display Logs: Expanded Full-Width Section (Excel-style)
#         st.divider()
        
#         if daily_log.foods:
#             st.header("Daily Food Log")
#             # Header
#             hcols = st.columns([0.5, 1.5, 3, 1.5, 1.5, 1, 1])
#             hcols[0].write("**#**")
#             hcols[1].write("**Meal**")
#             hcols[2].write("**Food Item**")
#             hcols[3].write("**Group**")
#             hcols[4].write("**Calories**")
#             hcols[5].write("**Portion**")
#             hcols[6].write("**Action**")
#             st.divider()

#             for i, f in enumerate(daily_log.foods):
#                 cols = st.columns([0.5, 1.5, 3, 1.5, 1.5, 1, 1])
#                 cols[0].write(f"{i+1}")
#                 cols[1].write(f.meal_type)
#                 cols[2].write(f.food_name)
#                 cols[3].write(f.food_group if f.food_group else "-")
#                 cols[4].write(f"{f.calories:.0f} kcal")
#                 cols[5].write(f"{f.portion}x")
#                 if cols[6].button("🗑️", key=f"del_food_{i}", help="Delete this entry"):
#                     if delete_food_entry(daily_log, i):
#                         st.rerun()
        
#         st.divider()
        
#         if daily_log.activities:
#             st.header("Daily Activity Log")
#             # Header
#             hcols = st.columns([0.5, 3, 3, 1.5, 1.5, 1])
#             hcols[0].write("**#**")
#             hcols[1].write("**Activity**")
#             hcols[2].write("**Motion**")
#             hcols[3].write("**Duration**")
#             hcols[4].write("**Burnt**")
#             hcols[5].write("**Action**")
#             st.divider()

#             for i, a in enumerate(daily_log.activities):
#                 cols = st.columns([0.5, 3, 3, 1.5, 1.5, 1])
#                 cols[0].write(f"{i+1}")
#                 cols[1].write(a.activity_name)
#                 cols[2].write(a.specific_motion if a.specific_motion else "-")
#                 cols[3].write(f"{a.duration_minutes:.0f}m")
#                 cols[4].write(f"{a.calories_burnt:.1f} kcal")
#                 if cols[5].button("🗑️", key=f"del_act_{i}", help="Delete this entry"):
#                     if delete_activity_entry(daily_log, i):
#                         st.rerun()
