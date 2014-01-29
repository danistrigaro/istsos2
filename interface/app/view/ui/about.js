/*
 * File: app/view/ui/about.js
 * Date: Tue Jan 28 2014 17:15:56 GMT+0100 (CET)
 *
 * This file was generated by Ext Designer version 1.2.3.
 * http://www.sencha.com/products/designer/
 *
 * This file will be auto-generated each and everytime you export.
 *
 * Do NOT hand edit this file.
 */

Ext.define('istsos.view.ui.about', {
    extend: 'Ext.form.Panel',

    border: 0,
    bodyPadding: 10,
    title: '',

    initComponent: function() {
        var me = this;

        Ext.applyIf(me, {
            items: [
                {
                    xtype: 'fieldset',
                    title: 'istSOS',
                    items: [
                        {
                            xtype: 'displayfield',
                            name: 'istsos_version',
                            fieldLabel: 'Version',
                            anchor: '100%'
                        },
                        {
                            xtype: 'displayfield',
                            id: 'updates',
                            name: 'istsos_message',
                            fieldLabel: 'Updates',
                            anchor: '100%'
                        },
                        {
                            xtype: 'displayfield',
                            hidden: true,
                            id: 'download',
                            name: 'download_url',
                            fieldLabel: 'Download',
                            anchor: '100%'
                        },
                        {
                            xtype: 'textareafield',
                            hidden: true,
                            id: 'changelog',
                            name: 'latest_istsos_changelog',
                            readOnly: true,
                            fieldLabel: 'Change log',
                            anchor: '100%'
                        }
                    ]
                },
                {
                    xtype: 'container',
                    html: '<p>istSOS (Istituto Scienze della Terra Sensor Observation Service) is an implementation of the Sensor Observation Service standard from Open Geospatial Consortium.\n</p>\n<p>\nThe developement of istSOS has started in 2009 in order to provide a simple implementation of the SOS standard for the management, provision and integration of hydro-meteorological data collected in Canton Ticino (Switzerland).\n</p>\n<p>\nistSOS is entirely written in <a href="http://python.org/" target="_blank" rel="nofollow">Python</a> and is based on:\n</p>\n<ul>\n<li><a href="http://www.postgresql.org/" target="_blank" rel="nofollow">PostgreSQL\n</a> / <a href="http://postgis.refractions.net/" rel="nofollow">PostGIS\n</a></li>\n<li><a href="http://www.apache.org/" target="_blank" rel="nofollow">Apache\n</a> / <a href="http://code.google.com/p/modwsgi/">mod_wsgi\n</a></li>\n</ul>',
                    padding: '10 0 0 0',
                    styleHtmlContent: true,
                    anchor: '100%'
                }
            ]
        });

        me.callParent(arguments);
    }
});