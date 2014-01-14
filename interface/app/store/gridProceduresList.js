/*
 * File: app/store/gridProceduresList.js
 * Date: Tue Jan 14 2014 10:49:25 GMT+0100 (CET)
 *
 * This file was generated by Ext Designer version 1.2.3.
 * http://www.sencha.com/products/designer/
 *
 * This file will be auto-generated each and everytime you export.
 *
 * Do NOT hand edit this file.
 */

Ext.define('istsos.store.gridProceduresList', {
    extend: 'Ext.data.Store',

    constructor: function(cfg) {
        var me = this;
        cfg = cfg || {};
        me.callParent([Ext.apply({
            storeId: 'procedurelist',
            proxy: {
                type: 'ajax',
                reader: {
                    type: 'json',
                    idProperty: 'name',
                    root: 'data'
                }
            },
            fields: [
                {
                    name: 'name',
                    sortType: 'asText',
                    type: 'string'
                },
                {
                    name: 'description',
                    sortType: 'asText',
                    type: 'string'
                },
                {
                    name: 'sensortype',
                    sortType: 'asText',
                    type: 'string'
                },
                {
                    name: 'offerings'
                },
                {
                    name: 'observedproperties'
                },
                {
                    name: 'samplingTime'
                }
            ]
        }, cfg)]);
    }
});