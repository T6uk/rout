import streamlit as st
from dataclasses import asdict
from typing import List
from models import DietPlan, Meal, dict_to_diet_plan, generate_id
from data_manager import get_data_manager


def render_diet_plans_page():
    """Render the complete diet plans page"""
    st.title("🥗 Diet Plans")

    tab1, tab2, tab3 = st.tabs(["View Plans", "Create Plan", "Manage Plans"])

    with tab1:
        render_view_diets()

    with tab2:
        render_create_diet()

    with tab3:
        render_manage_diets()


def render_view_diets():
    """Render the view diet plans tab"""
    st.subheader("Your Diet Plans")
    dm = get_data_manager()
    diets_data = dm.load_diets()

    if diets_data:
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            calorie_filter = st.selectbox("Filter by Calories",
                                          ["All", "≤1500 cal", "1501-2000 cal", "2001-2500 cal", ">2500 cal"])
        with col2:
            meal_count_filter = st.selectbox("Filter by Meal Count",
                                             ["All", "1-3 meals", "4-6 meals", "7+ meals"])

        # Apply filters
        filtered_diets = filter_diets(diets_data, calorie_filter, meal_count_filter)

        if filtered_diets:
            for diet_data in filtered_diets:
                diet = dict_to_diet_plan(diet_data)
                render_diet_card(diet)
        else:
            st.info("No diet plans match your filter criteria.")
    else:
        st.info("No diet plans created yet! Go to 'Create Plan' tab to get started.")


def filter_diets(diets_data: List[dict], calorie_filter: str, meal_count_filter: str) -> List[dict]:
    """Apply filters to diet data"""
    filtered = diets_data

    if calorie_filter != "All":
        if calorie_filter == "≤1500 cal":
            filtered = [d for d in filtered if d['daily_calories'] <= 1500]
        elif calorie_filter == "1501-2000 cal":
            filtered = [d for d in filtered if 1501 <= d['daily_calories'] <= 2000]
        elif calorie_filter == "2001-2500 cal":
            filtered = [d for d in filtered if 2001 <= d['daily_calories'] <= 2500]
        elif calorie_filter == ">2500 cal":
            filtered = [d for d in filtered if d['daily_calories'] > 2500]

    if meal_count_filter != "All":
        if meal_count_filter == "1-3 meals":
            filtered = [d for d in filtered if len(d['meals']) <= 3]
        elif meal_count_filter == "4-6 meals":
            filtered = [d for d in filtered if 4 <= len(d['meals']) <= 6]
        elif meal_count_filter == "7+ meals":
            filtered = [d for d in filtered if len(d['meals']) >= 7]

    return filtered


def render_diet_card(diet: DietPlan):
    """Render a single diet plan card"""
    with st.expander(f"🥗 {diet.name} - {diet.daily_calories} cal/day"):
        # Diet overview
        st.write(f"**Description:** {diet.description}")

        # Macronutrient breakdown
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Daily Calories", f"{diet.daily_calories}")
        with col2:
            st.metric("Protein", f"{diet.daily_protein}g")
        with col3:
            st.metric("Carbs", f"{diet.daily_carbs}g")
        with col4:
            st.metric("Fat", f"{diet.daily_fat}g")

        # Macros percentage breakdown
        total_cals_from_macros = (diet.daily_protein * 4) + (diet.daily_carbs * 4) + (diet.daily_fat * 9)
        if total_cals_from_macros > 0:
            protein_pct = (diet.daily_protein * 4 / total_cals_from_macros) * 100
            carbs_pct = (diet.daily_carbs * 4 / total_cals_from_macros) * 100
            fat_pct = (diet.daily_fat * 9 / total_cals_from_macros) * 100

            st.write(f"**Macro Split:** Protein {protein_pct:.1f}% | Carbs {carbs_pct:.1f}% | Fat {fat_pct:.1f}%")

        # Meals section
        st.write("---")
        st.write("**🍽️ Meals:**")

        total_meal_calories = 0
        for i, meal in enumerate(diet.meals, 1):
            render_meal_summary(meal, i)
            total_meal_calories += meal.calories

        # Calorie verification
        if total_meal_calories != diet.daily_calories:
            st.warning(f"⚠️ Note: Individual meals total {total_meal_calories} calories, "
                       f"but daily target is {diet.daily_calories} calories.")


def render_meal_summary(meal: Meal, meal_number: int):
    """Render a summary of a single meal"""
    with st.container():
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(f"**{meal_number}. {meal.name}**")
            if meal.ingredients:
                ingredients_text = ", ".join(meal.ingredients[:3])
                if len(meal.ingredients) > 3:
                    ingredients_text += f" +{len(meal.ingredients) - 3} more"
                st.write(f"   🥘 *{ingredients_text}*")
            if meal.notes:
                st.write(f"   💡 *{meal.notes}*")
        with col2:
            st.write(f"**{meal.calories} cal**")
            st.write(f"P: {meal.protein}g | C: {meal.carbs}g | F: {meal.fat}g")
        st.write("---")


def render_create_diet():
    """Render the create diet form"""
    st.subheader("Create New Diet Plan")
    dm = get_data_manager()

    with st.form("create_diet", clear_on_submit=True):
        # Basic diet info
        col1, col2 = st.columns(2)
        with col1:
            diet_name = st.text_input("Diet Plan Name*", placeholder="e.g., Balanced Weekly Plan")
        with col2:
            num_meals = st.number_input("Number of meals", min_value=1, max_value=10, value=3)

        diet_desc = st.text_area("Description*", placeholder="Describe the purpose and goals of this diet plan...")

        # Daily targets
        st.write("---")
        st.write("**📊 Daily Nutritional Targets**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            daily_calories = st.number_input("Daily Calories*", min_value=1000, max_value=5000, value=2000)
        with col2:
            daily_protein = st.number_input("Daily Protein (g)*", min_value=50, max_value=300, value=150)
        with col3:
            daily_carbs = st.number_input("Daily Carbs (g)*", min_value=50, max_value=500, value=250)
        with col4:
            daily_fat = st.number_input("Daily Fat (g)*", min_value=30, max_value=200, value=70)

        # Show macro percentages
        total_cals_from_macros = (daily_protein * 4) + (daily_carbs * 4) + (daily_fat * 9)
        if total_cals_from_macros > 0:
            protein_pct = (daily_protein * 4 / total_cals_from_macros) * 100
            carbs_pct = (daily_carbs * 4 / total_cals_from_macros) * 100
            fat_pct = (daily_fat * 9 / total_cals_from_macros) * 100

            st.info(f"**Macro Split:** Protein {protein_pct:.1f}% | Carbs {carbs_pct:.1f}% | Fat {fat_pct:.1f}% "
                    f"(Total: {total_cals_from_macros:.0f} calories from macros)")

        # Meals section
        st.write("---")
        st.write("**🍽️ Meals**")

        meals = []
        total_meal_calories = 0

        for i in range(num_meals):
            with st.container():
                st.write(f"**Meal {i + 1}**")

                col1, col2 = st.columns(2)
                with col1:
                    meal_name = st.text_input("Meal Name*", key=f"meal_name_{i}",
                                              placeholder="e.g., Breakfast")
                with col2:
                    meal_calories = st.number_input("Calories*", key=f"meal_cal_{i}",
                                                    min_value=0, max_value=2000, value=500)

                # Macronutrients
                col1, col2, col3 = st.columns(3)
                with col1:
                    meal_protein = st.number_input("Protein (g)*", key=f"meal_prot_{i}",
                                                   min_value=0.0, max_value=100.0, value=25.0, step=0.5)
                with col2:
                    meal_carbs = st.number_input("Carbs (g)*", key=f"meal_carbs_{i}",
                                                 min_value=0.0, max_value=150.0, value=50.0, step=0.5)
                with col3:
                    meal_fat = st.number_input("Fat (g)*", key=f"meal_fat_{i}",
                                               min_value=0.0, max_value=50.0, value=15.0, step=0.5)

                # Additional meal info
                meal_ingredients = st.text_input("Ingredients (comma-separated)", key=f"meal_ing_{i}",
                                                 placeholder="chicken breast, rice, broccoli")
                meal_notes = st.text_input("Notes", key=f"meal_notes_{i}",
                                           placeholder="Preparation notes, timing, etc.")

                if meal_name:
                    ingredients_list = [ing.strip() for ing in meal_ingredients.split(',') if ing.strip()]
                    meals.append(Meal(
                        id=generate_id(),
                        name=meal_name,
                        calories=meal_calories,
                        protein=meal_protein,
                        carbs=meal_carbs,
                        fat=meal_fat,
                        ingredients=ingredients_list,
                        notes=meal_notes
                    ))
                    total_meal_calories += meal_calories

                st.write("---")

        # Show total from meals vs target
        if meals:
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Total from meals:** {total_meal_calories} calories")
            with col2:
                st.write(f"**Daily target:** {daily_calories} calories")

            if abs(total_meal_calories - daily_calories) > 50:
                st.warning("⚠️ There's a significant difference between your daily target and meal totals.")

        # Submit button
        submitted = st.form_submit_button("Create Diet Plan", type="primary")

        if submitted:
            if diet_name and diet_desc and meals:
                new_diet = DietPlan(
                    id=generate_id(),
                    name=diet_name,
                    description=diet_desc,
                    meals=meals,
                    daily_calories=daily_calories,
                    daily_protein=daily_protein,
                    daily_carbs=daily_carbs,
                    daily_fat=daily_fat
                )

                diets_data = dm.load_diets()
                diets_data.append(asdict(new_diet))

                if dm.save_diets(diets_data):
                    st.success(f"✅ Diet plan '{diet_name}' created successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Failed to save diet plan. Please try again.")
            else:
                st.error("⚠️ Please fill in the diet name, description, and at least one meal.")


def render_manage_diets():
    """Render the manage diets tab"""
    st.subheader("Manage Diet Plans")
    dm = get_data_manager()
    diets_data = dm.load_diets()

    if not diets_data:
        st.info("No diet plans to manage! Create some diet plans first.")
        return

    # Select diet to manage
    diet_options = {f"{d['name']} - {d['daily_calories']} cal": d['id'] for d in diets_data}
    selected_diet_name = st.selectbox("Select diet plan:", list(diet_options.keys()))

    if selected_diet_name:
        selected_diet_id = diet_options[selected_diet_name]
        diet_data = next(d for d in diets_data if d['id'] == selected_diet_id)
        diet = dict_to_diet_plan(diet_data)

        # Show diet details
        st.write("---")
        st.write("**Diet Plan Details:**")

        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Name:** {diet.name}")
            st.write(f"**Daily Calories:** {diet.daily_calories}")
            st.write(f"**Meals:** {len(diet.meals)} total")
        with col2:
            st.write(f"**Daily Protein:** {diet.daily_protein}g")
            st.write(f"**Daily Carbs:** {diet.daily_carbs}g")
            st.write(f"**Daily Fat:** {diet.daily_fat}g")

        st.write(f"**Description:** {diet.description}")

        # Quick meal overview
        with st.expander("Quick Meal Overview"):
            for i, meal in enumerate(diet.meals, 1):
                st.write(f"{i}. **{meal.name}** - {meal.calories} cal "
                         f"(P: {meal.protein}g, C: {meal.carbs}g, F: {meal.fat}g)")

        # Nutrition analysis
        with st.expander("Nutrition Analysis"):
            total_meal_calories = sum(meal.calories for meal in diet.meals)
            total_meal_protein = sum(meal.protein for meal in diet.meals)
            total_meal_carbs = sum(meal.carbs for meal in diet.meals)
            total_meal_fat = sum(meal.fat for meal in diet.meals)

            col1, col2 = st.columns(2)
            with col1:
                st.write("**From Individual Meals:**")
                st.write(f"Calories: {total_meal_calories}")
                st.write(f"Protein: {total_meal_protein}g")
                st.write(f"Carbs: {total_meal_carbs}g")
                st.write(f"Fat: {total_meal_fat}g")
            with col2:
                st.write("**Daily Targets:**")
                st.write(f"Calories: {diet.daily_calories}")
                st.write(f"Protein: {diet.daily_protein}g")
                st.write(f"Carbs: {diet.daily_carbs}g")
                st.write(f"Fat: {diet.daily_fat}g")

        # Action buttons
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🗑️ Delete Diet Plan", type="secondary"):
                if dm.delete_diet(selected_diet_id):
                    st.success("✅ Diet plan deleted successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to delete diet plan.")

        with col2:
            if st.button("📋 Duplicate Diet Plan", type="secondary"):
                # Create a copy
                new_diet = DietPlan(
                    id=generate_id(),
                    name=f"{diet.name} (Copy)",
                    description=diet.description,
                    meals=[Meal(
                        id=generate_id(),
                        name=meal.name,
                        calories=meal.calories,
                        protein=meal.protein,
                        carbs=meal.carbs,
                        fat=meal.fat,
                        ingredients=meal.ingredients.copy(),
                        notes=meal.notes
                    ) for meal in diet.meals],
                    daily_calories=diet.daily_calories,
                    daily_protein=diet.daily_protein,
                    daily_carbs=diet.daily_carbs,
                    daily_fat=diet.daily_fat
                )

                diets_data.append(asdict(new_diet))
                if dm.save_diets(diets_data):
                    st.success("✅ Diet plan duplicated successfully!")
                    st.rerun()

        with col3:
            if st.button("📊 Export Diet Plan", type="secondary"):
                import json
                diet_json = json.dumps(asdict(diet), indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=diet_json,
                    file_name=f"{diet.name.replace(' ', '_')}_diet.json",
                    mime="application/json"
                )


def get_diet_stats():
    """Get diet statistics for dashboard"""
    dm = get_data_manager()
    diets_data = dm.load_diets()

    if not diets_data:
        return None

    total_diets = len(diets_data)
    avg_calories = sum(d['daily_calories'] for d in diets_data) / total_diets
    total_meals = sum(len(d['meals']) for d in diets_data)

    return {
        "total": total_diets,
        "avg_calories": round(avg_calories, 0),
        "total_meals": total_meals,
        "avg_meals_per_plan": round(total_meals / total_diets, 1)
    }