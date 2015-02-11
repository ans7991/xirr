var Manager = Ember.Application.create();
var port = "8085";
var host = "localhost";

Manager.TransactionsEditController = Ember.ObjectController.extend({
  	types: ["BUY", "SELL"]
});

Manager.TransactionsNewController = Ember.ObjectController.extend({
	model: {},
	message: "",
  	types: ["BUY", "SELL"]
});

Manager.Router.map(function() {
	this.resource('transactions', function(){
		this.route('all');
		this.route('new');
		this.route('edit', {path: '/:id'});
	})
	
	this.resource('home', {path: '/'});
});

Manager.TransactionsAllRoute = Ember.Route.extend({
  	model: function() {
    	return jQuery.getJSON("http://"+host+":"+port+"/transactions");
  	},

  	actions : {
		delete : function(params) {
			var self = this;
			$.ajax({
				url: "http://"+host+":"+port+"/transactions/"+params.id,
				type: "DELETE"
			})
			.done(function(){
				self.refresh();
			})
		}
	}
});

Manager.TransactionsNewRoute = Ember.Route.extend({
	model: function() {
    	return jQuery.getJSON("http://"+host+":"+port+"/currentId").then(function(data){
    		return Manager.TransactionsNewRoute.create({}).set('id', data.seq);
		});
  	},

	actions : {
 	   insert : function() {
 	   		var self = this;
 	   		var transaction = this.modelFor("transactions.new");
 	   		$.ajax({
 	   			url: "http://"+host+":"+port+"/transactions", 
 	   			data: JSON.stringify(transaction),
 	   			type: "POST",
 	   			contentType: "application/json"
 	   		})
 	   		.done(function(data){
 	   			self.controllerFor('transactions.new').set('message', data.message);
 	   			setInterval(function(){
 	   				self.controllerFor('transactions.new').set('message', "");
 	   			}, 5000)
 	   		})
    	}
	}
});

Manager.TransactionsEditRoute = Ember.Route.extend({
	model: function(params) {
		return jQuery.getJSON("http://"+host+":"+port+"/transactions/"+ params.id);
	},

	actions : {
 	   update : function(params) {
 	   		var self = this;
 	   		var transaction = this.modelFor("transactions.edit");
 	   		$.ajax({
 	   			url: "http://"+host+":"+port+"/transactions/"+params.id, 
 	   			data: JSON.stringify(transaction),
 	   			type: "POST",
 	   			contentType: "application/json"
 	   		})
 	   		.done(function(){
 	   			self.transitionTo("transactions.all");
 	   		})
    	}
	}
});