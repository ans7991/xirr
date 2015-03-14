var Manager = Ember.Application.create();
var port = "8085";
var host = "localhost";

Manager.TransactionsEditController = Ember.ObjectController.extend({
  	types: ["BUY", "SELL"]
});

Manager.TransactionsNewController = Ember.ObjectController.extend({
	model: {},
  	types: ["BUY", "SELL"]
});

Manager.TransactionsSummaryController = Ember.ObjectController.extend({
	model: {}
});

Manager.Router.map(function() {
	this.resource('transactions', function(){
		this.route('all');
		this.route('new');
		this.route('edit', {path: '/:id'});
		this.route('summary');
	})
	
	this.resource('home', {path: '/'});
});

Manager.TransactionsSummaryRoute = Ember.Route.extend({
  	actions : {
  		getSummary : function(params) {
  			var self = this;
	    	return jQuery.getJSON("http://"+host+":"+port+"/summary?amount="+params.amount).then(function(data) {
	    		self.controllerFor('transactions.summary').set('model', data);
	    		console.log(self);
	    	})
  		}
  	}
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
 	   		.done(function(){
 	   			self.transitionTo("transactions.all");
 	   		})
    	},

    	upload: function() {
    		var self = this;
    		var file = new FormData();
    		file.append('upload', $('#uploadFile')[0].files[0]);
    		$.ajax({
 	   			url: "http://"+host+":"+port+"/upload", 
 	   			data: file,
 	   			type: "POST",
 	   			processData: false,
 	   			contentType: false
 	   		})
 	   		.done(function(){
 	   			self.transitionTo("transactions.all");
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

Ember.Handlebars.helper('total', function(quantity, price) {
  return (quantity * price).toFixed(2);
});

Ember.Handlebars.helper('commission', function(quantity, price) {
  return (quantity * price * 0.007).toFixed(2);
});

Ember.Handlebars.helper('net', function(quantity, price, type) {
	return type === 'BUY' ? (quantity * price * 1.007).toFixed(2) : (quantity * price * 0.993).toFixed(2);
});

Ember.Handlebars.helper('net', function(sell, buy) {
  return (sell + buy).toFixed(2);
});