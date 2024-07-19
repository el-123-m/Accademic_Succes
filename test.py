# import plotly.express as px
# import plotly.graph_objects as go
# import pandas as pd

# # Sample filtered_data
# filtered_data = pd.DataFrame({
#     'Gender': ['Male', 'Female', 'Other'],
#     'Count': [50, 40, 10]
# })

# # Create a pie chart
# fig_gender = go.Figure()

# # Add pie trace
# fig_gender.add_trace(go.Pie(
#     labels=filtered_data['Gender'],
#     values=filtered_data['Count'],
#     hole=0.4,
#     textinfo='label+percent',
#     insidetextorientation='radial',
#     marker=dict(colors=['#FF0000', '#000000', '#AAAAAA']),
#     hoverinfo='label+percent+value',
#     rotation=90
# ))

# # Update layout with more advanced features
# fig_gender.update_layout(
#     title_text='Gender Distribution',
#     annotations=[dict(text='Gender Distribution', x=0.5, y=0.5, font_size=20, showarrow=False)],
#     showlegend=True,
#     legend_title_text='Gender Categories',
#     legend=dict(
#         x=0.85,
#         y=0.5,
#         traceorder='normal',
#         font=dict(size=12),
#         bgcolor='rgba(255, 255, 255, 0.5)',
#     ),
#     margin=dict(l=0, r=0, t=40, b=0),
#     autosize=True,
#     paper_bgcolor='rgba(240, 240, 240, 0.9)',
#     plot_bgcolor='rgba(255, 255, 255, 0.8)',
# )

# # Add a callback function if using Dash for interactivity
# # For example, if you were using Dash:
# # @app.callback(
# #     Output('output-div', 'children'),
# #     [Input('pie-chart', 'clickData')]
# # )
# # def display_click_data(clickData):
# #     if clickData is None:
# #         return "Click a slice"
# #     return f"Clicked on: {clickData['points'][0]['label']}"

# fig_gender.show()
