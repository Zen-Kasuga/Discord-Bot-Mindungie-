import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import pandas as pd
from tabulate import tabulate
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, root_mean_squared_error, r2_score
import matplotlib.pyplot as plot
import matplotlib as mpl

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default() #This shi filters what messages the bot WANT to receive

intents.message_content = True #Encryption thingy, it allows the bot to view discord messages

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def Analyze(ctx, y_variable):
    print(ctx.author)
    print(ctx.channel)
    print(ctx.guild)

    x_variable = []

    if not ctx.message.attachments:
        await ctx.send(f"There is no attachment, {ctx.author}. You dumb fuck!!")
        return 

    for attachment in ctx.message.attachments:
        if attachment.filename.endswith(".csv"):
            await attachment.save(attachment.filename)
            file_path = attachment.filename
            dataFrame = pd.read_csv(file_path)
            
            if y_variable in dataFrame.columns:
                for col in dataFrame.columns:
                    if col != y_variable:
                        x_variable.append(col)

                x_values = dataFrame[x_variable]
                y_values = dataFrame[y_variable]

                regression = LinearRegression().fit(x_values, y_values)
                prediction = regression.predict(x_values)
                mae = mean_absolute_error(y_values, prediction)
                mse = mean_squared_error(y_values, prediction)
                rmse = root_mean_squared_error(y_values, prediction)
                r2 = r2_score(y_values, prediction)

                coefficients = regression.coef_
                intercept = regression.intercept_

                dataFrame['Prediction'] = prediction

                charts = []

                for col in x_variable:
                    chart = plot.figure()
                    plot.scatter(dataFrame[col], y_values, color='#33415c')

                    chart_regression = LinearRegression().fit(x_values[[col]], y_values)

                    sort = dataFrame.sort_values(by=col)

                    chart_prediction = chart_regression.predict(sort[[col]])
                    
                    plot.plot(sort[col], chart_prediction, color='#001233', linewidth=2)
                    plot.legend()

                    plot.title(f"Regression of {col} vs {y_variable}")
                    plot.xlabel(col)
                    plot.ylabel(y_variable)

                    chart.savefig(f"{col}_vs_{y_variable}.png")
                    charts.append(f"{col}_vs_{y_variable}.png")

                    plot.close(chart)

                await ctx.send(f"```text\nRegression Results:\n\n{dataFrame.to_markdown(index=False)}\n```")
                await ctx.send(f"```text\nCoefficients: {coefficients}\nIntercept: {intercept}\nMean Absolute Error (MAE): {mae}\nMean Squared Error (MSE): {mse}\nRoot Mean Squared Error (RMSE): {rmse}\nR-squared (R2): {r2}\n```")
                for chart_file in charts:
                    await ctx.send(file=discord.File(chart_file))
                    os.remove(chart_file)
                    os.remove(file_path)
            else:
                await ctx.send(f"The column '{y_variable}' does not exist in the CSV file, {ctx.author}. You bitch!!")

        else:
            await ctx.send(f"This is not a csv file, {ctx.author}. You dumb fuck!!")

@bot.command()
async def Bar(ctx, x_variable_bar, y_variable_bar):
    print(ctx.author)
    print(ctx.channel)
    print(ctx.guild)

    if not ctx.message.attachments:
        await ctx.send(f"There is no attachment, {ctx.author}. You dumb fuck!!")
        return

    for attachment in ctx.message.attachments:
        if attachment.filename.endswith(".csv"):
            await attachment.save(attachment.filename)
            file_path = attachment.filename
            dataFrame = pd.read_csv(file_path)

            if y_variable_bar in dataFrame.columns and x_variable_bar in dataFrame.columns:
                x_values = dataFrame[x_variable_bar]
                y_values = dataFrame[y_variable_bar]

                fig, ax = plot.subplots()
                ax.bar(x_values, y_values, color='#a4133c')

                plot.title(f"Bar Chart of {y_variable_bar} vs {x_variable_bar}")
                plot.xlabel(x_variable_bar)
                plot.ylabel(y_variable_bar)

                filename = "BarChart.png"

                fig.savefig(filename)
                await ctx.send(file=discord.File(filename))

                plot.close(fig)
                os.remove(filename)
                os.remove(file_path)

                return
            else:
                await ctx.send(f"The columns '{x_variable_bar}' or '{y_variable_bar}' do not exist in the CSV file. {ctx.author}, You bitch!!")
                return
    else:
        await ctx.send(f"This is not a csv file, {ctx.author}. You dumb fuck!!")

@bot.command()
async def Pie(ctx, x_variable_pie, y_variable_pie):
    print(ctx.author)
    print(ctx.channel)
    print(ctx.guild)

    colors = [
        "#ffccd5",
        "#ffb3c1",
        "#ff8fa3",
        "#ff758f",
        "#ff4d6d",
        "#c9184a",
        "#a4133c",
        "#800f2f",
        "#590d22",
        "#000000"  
    ]

    if not ctx.message.attachments:
        await ctx.send(f"There is no attachment, {ctx.author}. You dumb fuck!!")
        return

    for attachment in ctx.message.attachments:
        if attachment.filename.endswith(".csv"):
            await attachment.save(attachment.filename)
            file_path = attachment.filename
            dataFrame = pd.read_csv(file_path)

            if y_variable_pie in dataFrame.columns and x_variable_pie in dataFrame.columns:
                x_values = dataFrame[x_variable_pie]
                y_values = dataFrame[y_variable_pie]

                x_variable_pie = dataFrame.columns[0]
                y_variable_pie = dataFrame.columns[1]
                
                x_values = dataFrame[x_variable_pie]
                y_values = dataFrame[y_variable_pie]
                            
                fig, ax = plot.subplots()
                ax.pie(y_values, labels=x_values, colors=colors, autopct='%1.1f%%')
                
                plot.title(f"Pie Chart of {y_variable_pie} vs {x_variable_pie}")
                
                filename = "PieChart.png"
                
                fig.savefig(filename)
                await ctx.send(file=discord.File(filename))
                
                plot.close(fig)
                os.remove(filename)
                os.remove(file_path)
            else:
                await ctx.send(f"The columns '{x_variable_pie}' or '{y_variable_pie}' do not exist in the CSV file. {ctx.author}, You bitch!!")
                return
        else:
            await ctx.send(f"This is not a csv file, {ctx.author}. You dumb fuck!!")

@bot.command()
async def Scatter(ctx, x_variable_scatter, y_variable_scatter):
    print(ctx.author)
    print(ctx.channel)
    print(ctx.guild)

    if not ctx.message.attachments:
        await ctx.send(f"There is no attachment, {ctx.author}. You dumb fuck!!")
        return

    for attachment in ctx.message.attachments:
        if attachment.filename.endswith(".csv"):
            await attachment.save(attachment.filename)
            file_path = attachment.filename
            dataFrame = pd.read_csv(file_path)

            if y_variable_scatter in dataFrame.columns and x_variable_scatter in dataFrame.columns:
                x_values = dataFrame[x_variable_scatter]
                y_values = dataFrame[y_variable_scatter]

                fig, ax = plot.subplots()
                ax.scatter(x_values, y_values, color='#590d22')

                plot.title(f"Scatter Plot of {y_variable_scatter} vs {x_variable_scatter}")
                plot.xlabel(x_variable_scatter)
                plot.ylabel(y_variable_scatter)

                filename = "ScatterPlot.png"

                fig.savefig(filename)
                await ctx.send(file=discord.File(filename))

                plot.close(fig)
                os.remove(filename)
                os.remove(file_path)

                return
            else:
                await ctx.send(f"The columns '{x_variable_scatter}' or '{y_variable_scatter}' do not exist in the CSV file. {ctx.author}, You bitch!!")
                return
    else:
        await ctx.send(f"This is not a csv file, {ctx.author}. You dumb fuck!!")

@bot.command()
async def Line(ctx, x_variable_line, y_variable_line):
    print(ctx.author)
    print(ctx.channel)
    print(ctx.guild)

    if not ctx.message.attachments:
        await ctx.send(f"There is no attachment, {ctx.author}. You dumb fuck!!")
        return

    for attachment in ctx.message.attachments:
        if attachment.filename.endswith(".csv"):
            await attachment.save(attachment.filename)
            file_path = attachment.filename
            dataFrame = pd.read_csv(file_path)

            if y_variable_line in dataFrame.columns and x_variable_line in dataFrame.columns:

                dataFrame = dataFrame.sort_values(by=x_variable_line)

                x_values = dataFrame[x_variable_line]
                y_values = dataFrame[y_variable_line]

                fig, ax = plot.subplots()
                ax.plot(x_values, y_values, color='#800f2f', linewidth=2)

                plot.title(f"Line Chart of {y_variable_line} vs {x_variable_line}")
                plot.xlabel(x_variable_line)
                plot.ylabel(y_variable_line)

                filename = "LineChart.png"

                fig.savefig(filename)
                await ctx.send(file=discord.File(filename))

                plot.close(fig)
                os.remove(filename)
                os.remove(file_path)

                return
            else:
                await ctx.send(f"The columns '{x_variable_line}' or '{y_variable_line}' do not exist in the CSV file. {ctx.author}, You bitch!!")
                return
    else:
        await ctx.send(f"This is not a csv file, {ctx.author}. You dumb fuck!!")

@bot.command()
async def Mindungie(ctx):
    print(ctx.author)
    print(ctx.channel)
    print(ctx.guild)
    await ctx.send("Wassap Bitch!!")

@bot.command()
async def yo(ctx):
    print(ctx.author)
    print(ctx.channel)
    print(ctx.guild)
    await ctx.send("Yahalloooooo")

bot.run(TOKEN)