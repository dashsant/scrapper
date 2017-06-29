/**
 * This class is the main view for the application. It is specified in app.js as the
 * "mainView" property. That setting automatically applies the "viewport"
 * plugin causing this view to become the body element (i.e., the viewport).
 *
 * TODO - Replace this content of this view to suite the needs of your application.
 */
Ext.define('newsscraper.view.main.Main', {
    extend: 'Ext.panel.Panel',
    xtype: 'app-main',
    layout: 'border',
    height:"100%",
    width:"100%",
    header:false,
    requires: [
        'Ext.plugin.Viewport',
        'Ext.window.MessageBox',

        'newsscraper.view.main.MainController',
        'newsscraper.view.main.MainModel'
    ],

    controller: 'main',
    viewModel: 'main',
    items: [
     {
        header: false,
	region: 'south',     // position for region
        xtype: 'panel',
	split:true,
	splitterResize:false,
	height:"80%",
        //layout: 'fit',
        margin: '0 5 5 5'
    },
    {
        title: 'Center Region',
        region: 'center',     // center region is required, no width/height specified
        xtype: 'panel',
        height: 100,
        margin: '5 5 0 0',
	bbar: [ { xtype: 'button', text: 'Most Recent'} ,  
		{ xtype: 'button', text: 'Last 1 weeks'} ,  
		{ xtype: 'button', text: 'Last 2 weeks'} ,
		{ xtype: 'button', text: 'Last 3 weeks'} ,
		{ xtype: 'button', text: 'Last 4 weeks'} ,
		{ xtype: 'button', text: 'Custom'}
		],
    }
    ]

});
