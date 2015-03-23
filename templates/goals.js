var bar_max_width = 900;
var points_limit; //must be fetched from the database = (new savings) * (conversion constant) 
var data;

function drawChart()
{
	for (var i = 0; i<data.length; i++) 
	{	
		if (data[i].title !== "No Goal Set Yet")
		{
			var step = bar_max_width/data[i].total_value;
			var width = step * data[i].current_value;
		
			if (width >= bar_max_width*0.75) 
			{
				document.getElementById("bar" + (i+1)).style.backgroundColor = "MediumPurple";
				document.getElementById((i+1)).style.color = "MediumPurple";
			}
			if (width >= bar_max_width*0.5 && width < bar_max_width*0.75) 
			{
				document.getElementById("bar" + (i+1)).style.backgroundColor = "DodgerBlue";
				document.getElementById((i+1)).style.color = "DodgerBlue";
			}
			if (width >= bar_max_width*0.25 && width < bar_max_width*0.5) 
			{
				document.getElementById("bar" + (i+1)).style.backgroundColor = "DarkOrange ";
				document.getElementById((i+1)).style.color = "DarkOrange ";
			}
			if (width < bar_max_width*0.25) 
			{
				document.getElementById("bar" + (i+1)).style.backgroundColor = "FireBrick";
				document.getElementById((i+1)).style.color = "FireBrick";
			}
		
			document.getElementById("bar" + (i+1)).style.width = width + "px";
			var rem =  data[i].total_value - data[i].current_value;
			document.getElementById("bar" + (i+1)).innerHTML = "<strong>" + data[i].current_value + "/" + data[i].total_value + "</strong>";
			
			document.getElementById((i+1)).innerHTML = "<strong>" + (i+1) + " : " + data[i].title + " (" + rem + " left to save)" + "</strong>";
			
			if (data[i].current_value == data[i].total_value)
			{
				document.getElementById("wining_goal").innerHTML = "GOAL #" + (i+1);
			}
		}
		else
		{
			document.getElementById("bar" + (i+1)).style.backgroundColor = "#0B8C52";
			document.getElementById("bar" + (i+1)).style.width = 120 + "px";
			document.getElementById("bar" + (i+1)).innerHTML = data[i].title;
		}
	}
	
	document.getElementById("unused").innerHTML = "Unused : " + points_limit + " points";
}

function initialize()
{
	document.getElementById("add_goal_num").value = null;
	document.getElementById("add_goal_points").value = null;
	document.getElementById("from_goal_num").value = null;
	document.getElementById("to_goal_num").value = null;
	document.getElementById("move_goal_points").value = null;
	
	/*data saved from the last session
	 *to be fetched from the database */
	data = [
		{title: "Lego", total_value: 300, current_value: 140},
		{title: "DVD", total_value: 200, current_value:200},
		{title: "PS4", total_value: 900, current_value: 100},
		{title: "Ice Cream Maker", total_value: 600, current_value: 300}
	];
	points_limit = 200;
	drawChart();
}

function newGoal()
{
	/*inputs from the parent interface required: title, total_value*/
	var flag = true;
	var i = 0;
	while(flag && i<data.length)
	{
		if (data[i].title == "No Goal Set Yet")
		{
			data[i].title = "PS4";
			data[i].total_value = 900;
			data[i].current_value = 0;
			flag = false;
		}
		i++;
	}
	
	if (i == data.length) {alert("New Goal cannot be added! Wait till one goal to complete");}
	
	drawChart();
}

function goalIsComplete()
{
	/*invoked when prize has been claimed*/
	var flag = true;
	var i = 0;
	
	for(var i=0; i<data.length; i++)
	{
		if (data[i].current_value == data[i].total_value && data[i].current_value !== 0 && data[i].total_value != 0 && flag)
		{
			/*NOTIFY PARENT ACCOUNT and remove this goal from the chart*/
			window.confirm("Wohoo! Your parent/guardian has been notified about your achievement. Well Done, Mate!!!");
			data[i].title = "No Goal Set Yet";
			data[i].total_value = 0;
			data[i].current_value = 0;
			document.getElementById("wining_goal").innerHTML = " ";
			document.getElementById((i+1)).innerHTML = "<strong>" + (i+1) + " : " + " none " + "</strong>";
			document.getElementById((i+1)).style.color = "#0B8C52";
			flag = false;
		}
	}
	
	if (flag) {alert("Oops! Sorry, you haven't completed any goals yet.");}

	drawChart();
}

function addPoints()
{
	var goal = parseInt(document.getElementById("add_goal_num").value)-1; 
	var points = parseInt(document.getElementById("add_goal_points").value); 
	
	var new_value = data[goal].current_value + points;
	points_limit = points_limit - points;
	
	if (points_limit >= 0 && data[goal].title !== "No Goal Set Yet" && new_value <= data[goal].total_value)
	{
		data[goal].current_value = new_value;
	}
	else
	{
		alert("Action cannot be completed due to:\n-you have exceeded unused points limit\n-goal does not exist\n-you are about to exceed goal limit\nCheck you inputs again.");
	}
	
	drawChart();	
}

function movePoints()
{
	var from = parseInt(document.getElementById("from_goal_num").value)-1; 
	var to = parseInt(document.getElementById("to_goal_num").value)-1; 
	var points = parseInt(document.getElementById("move_goal_points").value); 
	
	var new_value_to = data[to].current_value + points;
	var new_value_from = data[from].current_value - points;
	
	if (new_value_from >= 0 
		&& data[from].title !== "No Goal Set Yet" 
		&& data[to].title !== "No Goal Set Yet" 
		&& new_value_to <= data[to].total_value)
	{
		if (data[from].current_value == data[from].total_value) 
		{
			document.getElementById("wining_goal").innerHTML = " ";
		}
		data[to].current_value = new_value_to;
		data[from].current_value = new_value_from;
	}
	else
	{
		alert("Action cannot be completed due to:\n-you have exceeded (from) goal points limit\n-goal(s) do(es) not exist\n-you are about to exceed (to) goal limit\n Check you inputs again.");
	}
	
	drawChart();	
}



