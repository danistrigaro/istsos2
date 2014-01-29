/*
 * File: app/view/ui/database.js
 * Date: Tue Jan 28 2014 17:15:56 GMT+0100 (CET)
 *
 * This file was generated by Ext Designer version 1.2.3.
 * http://www.sencha.com/products/designer/
 *
 * This file will be auto-generated each and everytime you export.
 *
 * Do NOT hand edit this file.
 */

Ext.define('istsos.view.ui.database', {
    extend: 'Ext.form.Panel',

    border: 0,
    bodyPadding: 10,
    title: '',

    initComponent: function() {
        var me = this;

        Ext.applyIf(me, {
            items: [
                {
                    xtype: 'displayfield',
                    hidden: true,
                    id: 'messageField',
                    fieldStyle: 'color: red;',
                    name: 'message',
                    fieldLabel: 'Message',
                    labelStyle: 'color: red;',
                    anchor: '100%'
                },
                {
                    xtype: 'fieldset',
                    title: 'PostGIS database',
                    items: [
                        {
                            xtype: 'textfield',
                            name: 'user',
                            fieldLabel: 'User',
                            anchor: '100%'
                        },
                        {
                            xtype: 'textfield',
                            inputType: 'password',
                            name: 'password',
                            fieldLabel: 'Password',
                            anchor: '100%'
                        },
                        {
                            xtype: 'textfield',
                            name: 'host',
                            fieldLabel: 'Host',
                            anchor: '100%'
                        },
                        {
                            xtype: 'textfield',
                            name: 'port',
                            fieldLabel: 'Port',
                            anchor: '100%'
                        },
                        {
                            xtype: 'textfield',
                            name: 'dbname',
                            fieldLabel: 'DB name',
                            anchor: '100%'
                        }
                    ]
                },
                {
                    xtype: 'container',
                    items: [
                        {
                            xtype: 'toolbar',
                            ui: 'footer',
                            layout: {
                                pack: 'center',
                                type: 'hbox'
                            },
                            items: [
                                {
                                    xtype: 'button',
                                    id: 'btnTestConnection',
                                    text: 'Test connection'
                                }
                            ]
                        }
                    ]
                }
            ]
        });

        me.callParent(arguments);
    }
});