import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# -----------------------------------
# Load the data
# -----------------------------------

orders = pd.read_csv("data/orders.csv")
customers = pd.read_csv("data/customers.csv")

# -----------------------------------
# Calculate KPI values
# -----------------------------------

total_revenue = orders["Revenue"].sum()
total_orders = orders["Order_ID"].nunique()
total_customers = customers["Customer_ID"].nunique()
total_profit = orders["Profit"].sum()
total_units = orders["Quantity"].sum()

# -----------------------------------
# Monthly Revenue Analysis
# -----------------------------------

orders["Order_Date"] = pd.to_datetime(orders["Order_Date"])

monthly_revenue = (
    orders
    .groupby(orders["Order_Date"].dt.to_period("M"))["Revenue"]
    .sum()
    .reset_index()
)

monthly_revenue["Order_Date"] = monthly_revenue["Order_Date"].astype(str)

revenue_chart = px.line(
    monthly_revenue,
    x="Order_Date",
    y="Revenue",
    markers=True,
    title="Monthly Revenue Trend"
)

revenue_chart.update_yaxes(
    tickprefix="₹",
    separatethousands=True
)

# -----------------------------------
# Category Revenue Analysis
# -----------------------------------

category_revenue = (
    orders
    .groupby("Category")["Revenue"]
    .sum()
    .reset_index()
    .sort_values("Revenue", ascending=False)
)

category_chart = px.bar(
    category_revenue,
    x="Category",
    y="Revenue",
    title="Revenue by Product Category",
    text_auto=True
)

category_chart.update_yaxes(
    tickprefix="₹",
    separatethousands=True
)

# -----------------------------------
# Regional Revenue Analysis
# -----------------------------------

region_revenue = (
    orders
    .groupby("Region")["Revenue"]
    .sum()
    .reset_index()
    .sort_values("Revenue", ascending=False)
)

region_chart = px.bar(
    region_revenue,
    x="Region",
    y="Revenue",
    title="Revenue by Region",
    text_auto=True
)

region_chart.update_yaxes(
    tickprefix="₹",
    separatethousands=True
)

# -----------------------------------
# Product Revenue Analysis
# -----------------------------------

product_revenue = (
    orders
    .groupby("Product")["Revenue"]
    .sum()
    .reset_index()
    .sort_values("Revenue", ascending=False)
)

product_chart = px.bar(
    product_revenue,
    x="Revenue",
    y="Product",
    orientation="h",
    title="Revenue by Product",
    text_auto=True
)

product_chart.update_xaxes(
    tickprefix="₹",
    separatethousands=True
)

# -----------------------------------
# Payment Method Analysis
# -----------------------------------

payment_data = (
    orders
    .groupby("Payment_Method")["Order_ID"]
    .count()
    .reset_index(name="Orders")
    .sort_values("Orders", ascending=False)
)

payment_chart = px.pie(
    payment_data,
    names="Payment_Method",
    values="Orders",
    title="Orders by Payment Method",
    hole=0.4
)

# -----------------------------------
# Customer Type Analysis
# -----------------------------------

customer_type_data = (
    customers
    .groupby("Customer_Type")["Customer_ID"]
    .count()
    .reset_index(name="Customers")
)

customer_type_chart = px.pie(
    customer_type_data,
    names="Customer_Type",
    values="Customers",
    title="New vs Returning Customers",
    hole=0.4
)

# -----------------------------------
# Top Customers by Spending
# -----------------------------------

customer_spending = (
    orders
    .groupby("Customer_ID")["Revenue"]
    .sum()
    .reset_index()
    .sort_values("Revenue", ascending=False)
    .head(10)
)

customer_spending = customer_spending.merge(
    customers[["Customer_ID", "Customer_Name"]],
    on="Customer_ID",
    how="left"
)

customer_spending_chart = px.bar(
    customer_spending.sort_values("Revenue"),
    x="Revenue",
    y="Customer_Name",
    orientation="h",
    title="Top 10 Customers by Spending",
    text_auto=True
)

customer_spending_chart.update_xaxes(
    tickprefix="₹",
    separatethousands=True
)

# -----------------------------------
# Filter Options
# -----------------------------------

category_options = [
    {"label": category, "value": category}
    for category in sorted(orders["Category"].unique())
]

region_options = [
    {"label": region, "value": region}
    for region in sorted(orders["Region"].unique())
]

payment_options = [
    {"label": payment, "value": payment}
    for payment in sorted(orders["Payment_Method"].unique())
]

# -----------------------------------
# Create Dash application
# -----------------------------------

app = Dash(__name__)

# -----------------------------------
# Dashboard layout
# -----------------------------------

app.layout = html.Div(
    [
        html.H1(
            "SmartCart E-Commerce Dashboard",
            style={
                "fontSize": "32px",
                "fontWeight": "700",
                "marginBottom": "5px",
                "color": "#111827"
            }
        ),

        html.P(
            "Sales and Customer Insights",
            style={
                "fontSize": "16px",
                "color": "#6b7280",
                "marginTop": "0px",
                "marginBottom": "20px"
            }
        ),

        html.Hr(),

        html.H2(
            "Dashboard Filters",
            style={
                "fontSize": "22px",
                "fontWeight": "600",
                "color": "#1f2937",
                "marginBottom": "15px"
            }
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.Label(
                            "Category",
                            style={
                                "fontWeight": "600",
                                "fontSize": "14px",
                                "color": "#374151",
                                "display": "block",
                                "marginBottom": "8px"
                            }
                        ),

                        dcc.Dropdown(
                            id="category-filter",
                            options=category_options,
                            placeholder="Select Category",
                            multi=True
                        )
                    ],
                    style={"width": "30%"}
                ),

                html.Div(
                    [
                        html.Label(
                            "Region",
                            style={
                                "fontWeight": "600",
                                "fontSize": "14px",
                                "color": "#374151",
                                "display": "block",
                                "marginBottom": "8px"
                            }
                        ),

                        dcc.Dropdown(
                            id="region-filter",
                            options=region_options,
                            placeholder="Select Region",
                            multi=True
                        )
                    ],
                    style={"width": "30%"}
                ),

                html.Div(
                    [
                        html.Label(
                            "Payment Method",
                            style={
                                "fontWeight": "600",
                                "fontSize": "14px",
                                "color": "#374151",
                                "display": "block",
                                "marginBottom": "8px"
                            }
                        ),

                        dcc.Dropdown(
                            id="payment-filter",
                            options=payment_options,
                            placeholder="Select Payment Method",
                            multi=True
                        )
                    ],
                    style={"width": "30%"}
                ),

                html.Div(
                    [
                        html.Label(
                            "Date Range",
                            style={
                                "fontWeight": "600",
                                "fontSize": "14px",
                                "color": "#374151",
                                "display": "block",
                                "marginBottom": "8px"
                            }
                        ),

                        dcc.DatePickerRange(
                            id="date-filter",
                            start_date=orders["Order_Date"].min(),
                            end_date=orders["Order_Date"].max(),
                            display_format="DD-MM-YYYY"
                        )
                    ],
                    style={"width": "30%"}
                )
            ],

            style={
                "display": "flex",
                "gap": "20px",
                "marginBottom": "30px",
                "flexWrap": "wrap",
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "12px",
                "boxShadow": "0 4px 12px rgba(0,0,0,0.06)"
            }
        ),

        html.Div(
            [
                html.H2(
                    "Key Performance Indicators",
                    style={
                        "fontSize": "22px",
                        "fontWeight": "600",
                        "color": "#1f2937",
                        "marginBottom": "15px"
                    }
                ),

                html.Div(
                    [
                        html.H3(
                            "Total Revenue",
                            style={
                                "fontSize": "15px",
                                "color": "#6b7280",
                                "marginBottom": "8px"
                            }
                        ),

                        html.H2(
                            f"₹{total_revenue:,.0f}",
                            id="total-revenue",
                            style={
                                "fontSize": "26px",
                                "color": "#111827",
                                "margin": "0"
                            }
                        )
                    ],
                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "12px",
                        "boxShadow": "0 4px 12px rgba(0,0,0,0.08)",
                        "flex": "1",
                        "minWidth": "150px",
                        "minHeight": "80px"
                    }
                ),

               html.Div(
                   [
                       html.H3(
                           "Total Orders",
                           style={
                               "fontSize": "15px",
                               "color": "#6b7280",
                               "marginBottom": "8px"
                           }
                       ),

                       html.H2(
                           f"{total_orders:,}",
                           id="total-orders",
                           style={
                               "fontSize": "26px",
                               "color": "#111827",
                               "margin": "0"
                           }
                       )
                    ],
                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "12px",
                        "boxShadow": "0 4px 12px rgba(0,0,0,0.08)",
                        "width": "180px",
                        "minHeight": "80px"
                    }
                ),

                html.Div(
                    [
                        html.H3(
                            "Total Customers",
                            style={
                                "fontSize": "15px",
                                "color": "#6b7280",
                                "marginBottom": "8px"
                            }
                        ),

                        html.H2(
                            f"{total_customers:,}",
                            id="total-customers",
                            style={
                                "fontSize": "26px",
                                "color": "#111827",
                                "margin": "0"
                            }
                        )
                    ],
                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "12px",
                        "boxShadow": "0 4px 12px rgba(0,0,0,0.08)",
                        "width": "180px",
                        "minHeight": "80px"
                    }
                ),

                html.Div(
                    [
                        html.H3(
                            "Total Profit",
                            style={
                                "fontSize": "15px",
                                "color": "#6b7280",
                                "marginBottom": "8px"
                            }
                        ),

                        html.H2(
                            f"₹{total_profit:,.0f}",
                            id="total-profit",
                            style={
                                "fontSize": "26px",
                                "color": "#111827",
                                "margin": "0"
                            }
                        )
                    ],
                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "12px",
                        "boxShadow": "0 4px 12px rgba(0,0,0,0.08)",
                        "width": "180px",
                        "minHeight": "80px"
                    }
                ),

                html.Div(
                    [
                        html.H3(
                            "Units Sold",
                            style={
                                "fontSize": "15px",
                                "color": "#6b7280",
                                "marginBottom": "8px"
                            }
                        ),

                        html.H2(
                            f"{total_units:,}",
                            id="total-units",
                            style={
                                "fontSize": "26px",
                                "color": "#111827",
                                "margin": "0"
                            }
                        )
                    ],
                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "12px",
                        "boxShadow": "0 4px 12px rgba(0,0,0,0.08)",
                        "width": "180px",
                        "minHeight": "80px"
                    }
                )
            ],

            style={
                "display": "flex",
                "gap": "20px",
                "flexWrap": "wrap",
                "marginBottom": "30px"
            }
        ),

        html.Br(),

        html.Div(
            dcc.Graph(
                id="revenue-chart",
                figure=revenue_chart
            ),
            style={
                "backgroundColor": "white",
                "borderRadius": "12px",
                "padding": "10px",
                "marginBottom": "20px",
                "boxShadow": "0 4px 12px rgba(0,0,0,0.08)"
            }
        ),

        html.Div(
            dcc.Graph(
                id="category-chart",
                figure=category_chart
            ),
            style={
                "backgroundColor": "white",
                "borderRadius": "12px",
                "padding": "10px",
                "marginBottom": "20px",
                "boxShadow": "0 4px 12px rgba(0,0,0,0.08)"
            }
        ),

        html.Div(
            dcc.Graph(
                id="region-chart",
                figure=region_chart
            ),
            style={
                "backgroundColor": "white",
                "borderRadius": "12px",
                "padding": "10px",
                "marginBottom": "20px",
                "boxShadow": "0 4px 12px rgba(0,0,0,0.08)"
            }
        ),

        html.Div(
            dcc.Graph(
                id="product-chart",
                figure=product_chart
            ),
            style={
                "backgroundColor": "white",
                "borderRadius": "12px",
                "padding": "10px",
                "marginBottom": "20px",
                "boxShadow": "0 4px 12px rgba(0,0,0,0.08)"
            }
        ),

        html.Div(
            dcc.Graph(
                id="payment-chart",
                figure=payment_chart
            ),
            style={
                "backgroundColor": "white",
                "borderRadius": "12px",
                "padding": "10px",
                "marginBottom": "20px",
                "boxShadow": "0 4px 12px rgba(0,0,0,0.08)"
            }
        ), 

        html.Div(
            dcc.Graph(
                id="customer-type-chart",
                figure=customer_type_chart
            ),
            style={
                "backgroundColor": "white",
                "borderRadius": "12px",
                "padding": "10px",
                "marginBottom": "20px",
                "boxShadow": "0 4px 12px rgba(0,0,0,0.08)"
            }
        ),

        html.Div(
            dcc.Graph(
                id="customer-spending-chart",
                figure=customer_spending_chart
            ),
            style={
                "backgroundColor": "white",
                "borderRadius": "12px",
                "padding": "10px",
                "marginBottom": "20px",
                "boxShadow": "0 4px 12px rgba(0,0,0,0.08)"
            }
        ),

        html.Hr(
            style={
                "marginTop": "40px",
                "marginBottom": "20px"
            }
        ),

        html.P(
            "SmartCart E-Commerce Dashboard | Built with Python, Dash & Plotly",
            style={
                "textAlign": "center",
                "color": "#6b7280",
                "fontSize": "14px",
                "marginBottom": "0"
            }
        )
    ],
    style={
        "backgroundColor": "#f4f7fb",
        "minHeight": "100vh",
        "padding": "30px",
        "fontFamily": "Arial, sans-serif",
        "boxSizing": "border-box"
    }
)

# -----------------------------------
# Interactive Dashboard Callback
# -----------------------------------

@app.callback(
    Output("total-revenue", "children"),
    Output("total-orders", "children"),
    Output("total-customers", "children"),
    Output("total-profit", "children"),
    Output("total-units", "children"),

    Output("revenue-chart", "figure"),
    Output("category-chart", "figure"),
    Output("region-chart", "figure"),
    Output("product-chart", "figure"),
    Output("payment-chart", "figure"),
    Output("customer-type-chart", "figure"),
    Output("customer-spending-chart", "figure"),

    Input("category-filter", "value"),
    Input("region-filter", "value"),
    Input("payment-filter", "value"),
    Input("date-filter", "start_date"),
    Input("date-filter", "end_date")
)
def update_dashboard(
    selected_categories,
    selected_regions,
    selected_payments,
    start_date,
    end_date
):

    # -----------------------------------
    # Filter the orders data
    # -----------------------------------

    filtered_orders = orders.copy()

    if selected_categories:
        filtered_orders = filtered_orders[
            filtered_orders["Category"].isin(selected_categories)
        ]

    if selected_regions:
        filtered_orders = filtered_orders[
            filtered_orders["Region"].isin(selected_regions)
        ]

    if selected_payments:
        filtered_orders = filtered_orders[
            filtered_orders["Payment_Method"].isin(selected_payments)
        ]

    if start_date:
        filtered_orders = filtered_orders[
            filtered_orders["Order_Date"] >= pd.to_datetime(start_date)
        ]

    if end_date:
        filtered_orders = filtered_orders[
            filtered_orders["Order_Date"] <= pd.to_datetime(end_date)
        ]
 
    # -----------------------------------
    # Updated KPI values
    # -----------------------------------

    revenue = filtered_orders["Revenue"].sum()

    order_count = filtered_orders["Order_ID"].nunique()

    units = filtered_orders["Quantity"].sum()

    profit = filtered_orders["Profit"].sum()

    customer_count = filtered_orders["Customer_ID"].nunique()

    # -----------------------------------
    # Monthly Revenue
    # -----------------------------------

    monthly = (
        filtered_orders
        .groupby(
            filtered_orders["Order_Date"].dt.to_period("M")
        )["Revenue"]
        .sum()
        .reset_index()
    )

    monthly["Order_Date"] = monthly["Order_Date"].astype(str)

    revenue_fig = px.line(
        monthly,
        x="Order_Date",
        y="Revenue",
        markers=True,
        title="Monthly Revenue Trend"
    )

    revenue_fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    revenue_fig.update_yaxes(
        tickprefix="₹",
        separatethousands=True
    )

    # -----------------------------------
    # Category Revenue
    # -----------------------------------

    category = (
        filtered_orders
        .groupby("Category")["Revenue"]
        .sum()
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )

    category_fig = px.bar(
        category,
        x="Category",
        y="Revenue",
        title="Revenue by Product Category",
        text_auto=True
    )

    category_fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    category_fig.update_yaxes(
        tickprefix="₹",
        separatethousands=True
    )

    # -----------------------------------
    # Regional Revenue
    # -----------------------------------

    region = (
        filtered_orders
        .groupby("Region")["Revenue"]
        .sum()
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )

    region_fig = px.bar(
        region,
        x="Region",
        y="Revenue",
        title="Revenue by Region",
        text_auto=True
    )

    region_fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    region_fig.update_yaxes(
        tickprefix="₹",
        separatethousands=True
    )

    # -----------------------------------
    # Product Revenue
    # -----------------------------------

    product = (
        filtered_orders
        .groupby("Product")["Revenue"]
        .sum()
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )

    product_fig = px.bar(
        product,
        x="Revenue",
        y="Product",
        orientation="h",
        title="Revenue by Product",
        text_auto=True
    )

    product_fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    product_fig.update_xaxes(
        tickprefix="₹",
        separatethousands=True
    )

    # -----------------------------------
    # Payment Method
    # -----------------------------------

    payment = (
        filtered_orders
        .groupby("Payment_Method")["Order_ID"]
        .count()
        .reset_index(name="Orders")
        .sort_values("Orders", ascending=False)
    )

    payment_fig = px.pie(
        payment,
        names="Payment_Method",
        values="Orders",
        title="Orders by Payment Method",
        hole=0.4
    )

    payment_fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # -----------------------------------
    # Customer Type
    # -----------------------------------

    filtered_customers = customers[
        customers["Customer_ID"].isin(
            filtered_orders["Customer_ID"]
        )
    ]

    customer_type = (
        filtered_customers
        .groupby("Customer_Type")["Customer_ID"]
        .count()
        .reset_index(name="Customers")
    )

    customer_type_fig = px.pie(
        customer_type,
        names="Customer_Type",
        values="Customers",
        title="New vs Returning Customers",
        hole=0.4
    )

    customer_type_fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # -----------------------------------
    # Top Customers
    # -----------------------------------

    top_customers = (
        filtered_orders
        .groupby("Customer_ID")["Revenue"]
        .sum()
        .reset_index()
        .sort_values("Revenue", ascending=False)
        .head(10)
    )

    top_customers = top_customers.merge(
        customers[["Customer_ID", "Customer_Name"]],
        on="Customer_ID",
        how="left"
    )

    top_customers_fig = px.bar(
        top_customers.sort_values("Revenue"),
        x="Revenue",
        y="Customer_Name",
        orientation="h",
        title="Top 10 Customers by Spending",
        text_auto=True
    )

    top_customers_fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    top_customers_fig.update_xaxes(
        tickprefix="₹",
        separatethousands=True
    )

    # -----------------------------------
    # Return updated dashboard
    # -----------------------------------

    return (
        f"₹{revenue:,.0f}",
        f"{order_count:,}",
        f"{customer_count:,}",
        f"₹{profit:,.0f}",
        f"{units:,}",

        revenue_fig,
        category_fig,
        region_fig,
        product_fig,
        payment_fig,
        customer_type_fig,
        top_customers_fig
    )

# -----------------------------------
# Run the application
# -----------------------------------

if __name__ == "__main__":
    app.run(debug=True)