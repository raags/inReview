/* Global vars */

var loadUrl = "review";
var selected = null;
var id = null;
var user_id = null;
var jsonUrl = "has_reviewed";
companyClass = "company-entry";
reviewLink = 'write-review';
reviewContent = 'write review';


/* Functions */


function getCompanies(values) {
	IN.API.Raw("/companies/" + values.company.id + ":(id,name,square-logo-url)").result(function(result) {

		$.getJSON(
		jsonUrl, 
		{'uid': user_id, 'cid' : values.company.id}, function(json) {
			
				if (result.squareLogoUrl == undefined) {
					logourl = "/static/undefined";
				} else {
					logourl = result.squareLogoUrl;
				}

				if (values.isCurrent) {
					positionPeriod = "Current";
				} else {
					positionPeriod = values.startDate.year + " - " + values.endDate.year;
				}
			
			logoHtml = "<img src=" + logourl + " alt=logo height=50 width=50 />"
			nameHtml = "<strong>" + result.name + "</strong>";
			dateHtml = "<em>" + positionPeriod + "</em>";
			
			if (json.response) {
				companyClass = "company-entry reviewed";
				reviewLink = "show-review";
				reviewContent = "Reviewed";
				iconHtml = "<i class='icon-check'></i>"
			} else {
				companyClass = "company-entry";
				reviewLink = "write-review";
				reviewContent = "Write Review";
				iconHtml = "<i class='icon-edit'></i>"
			}
				actionHtml = "<a class='" + reviewLink + "' id='" + values.company.id + "' href='#'>" + reviewContent + "</a>";
				htmldata = logoHtml + nameHtml + dateHtml + iconHtml + actionHtml;
				$("<li/>").appendTo("#company-list").html(htmldata).addClass(companyClass);
		});
		
	});
};

function loadCompanyList() {
		$("#company-list").empty();
	IN.API.Profile("me").fields(["id", "firstName", "lastName", "positions:(company:(id),start-date,end-date,is-current)"]).result(function(result) {
		data = result.values[0];
		user_id = data.id;
		greeting = "<p>Hello, <strong>" + data.firstName + " " + data.lastName + "&nbsp</strong>" + "<a href='#' id='logout'>[sign out]</a></p>";
		$("#sign-in").html(greeting)

		positionList = data.positions.values;
		$.each(positionList, function(index, values) {
			getCompanies(values);
		});
	});

};


$(document).on("click", "#logo", function() {
	$("#right").load("right");
});


$(document).on("click", ".write-review", function() {
	selected = $(this).siblings("strong").html();
	id = $(this).attr("id");
	$("#right").load("review");
	$(this).parent().addClass("selected").siblings().removeClass("selected");
});

$(document).on("click", ".show-review", function() {
	selected = $(this).siblings("strong").html();
	id = $(this).attr("id");
	$("#right").load("show", "id="+ id);
	$(this).parent().addClass("selected").siblings().removeClass("selected");
});


$(document).on("click", "#logout", function() {
	$("#sign-in").empty();
	$("#company-list").empty();
	$("#sign-in").append("<script type='IN/Login' data-size='large' data-onAuth='loadCompanyList'></script>");
	IN.User.logout();
	IN.init();
});




// For search

$(document).ready(function(){	 
$("#search").typeahead({
	source: ['LinkedIn', 'Red Hat', 'Yahoo!', 'Google']
 });
});


$(document).on("click", "#submit", function() {

searchVal = $("#search").val();

if (searchVal) {
switch(searchVal)
{
case "LinkedIn":
  id = 1337;
  break;
case "Red Hat":
  id = 3545;
  break;
case "Yahoo!":
  id = 1288;
  break;
case "Google":
  id = 1441;
  break;

  default:
  id = 1337;
}
}

$("#right").load("show", "id="+ id);

});
