document.addEventListener('DOMContentLoaded', function () {
    if (typeof django !== 'undefined' && django.jQuery) {
        (function ($) {
            $(document).ready(function () {
                function loadPluginForm(plugin, options) {
                    const url = `/admin/plugins/dynamic_form/${plugin}/`;
                    $.get(url, function (data) {
                        if (data) {
                            $('#dynamic-form-content').html(data);

                            // Populate the form with the existing options data
                            if (options) {
                                const parsedOptions = JSON.parse(options);

                                function populateFields(data, parentKey = '') {
                                    for (const key in data) {
                                        const fullKey = parentKey ? `${parentKey}__${key}` : key; // Use __ for nesting
                                        const field = $(`[name="${fullKey}"]`);
                                        if (field.length) {
                                            field.val(data[key]);
                                        } else if (typeof data[key] === 'object') {
                                            populateFields(data[key], fullKey); // Recurse for nested objects
                                        }
                                    }
                                }

                                populateFields(parsedOptions);
                            }
                        } else {
                            $('#dynamic-form-content').html('<p>Error loading form.</p>');
                        }
                    });
                }

                // Handle plugin change event
                $('#id_plugin').change(function () {
                    const plugin = $(this).val();
                    const options = $('#id_options').val();
                    if (!plugin) return;

                    loadPluginForm(plugin, options);
                });

                // Trigger an initial load if a plugin is already selected
                const initialPlugin = $('#id_plugin').val();
                const initialOptions = $('#id_options').val();
                if (initialPlugin) {
                    loadPluginForm(initialPlugin, initialOptions);
                }
            });

            // Before form submission, serialize the dynamic form data into the options field
            function setNestedValue(obj, path, value) {
                const keys = path.split('__'); // Split using __
                let current = obj;

                while (keys.length > 1) {
                    const key = keys.shift();
                    current[key] = current[key] || {};
                    current = current[key];
                }

                current[keys[0]] = value;
            }

            $('form').on('submit', function () {
                const dynamicFormData = {};
                $('#dynamic-form-content')
                    .find(':input')
                    .each(function () {
                        const key = $(this).attr('name');
                        const value = $(this).val();

                        if (key) {
                            setNestedValue(dynamicFormData, key, value);
                        }
                    });

                $('#id_options').val(JSON.stringify(dynamicFormData));
            });

        })(django.jQuery);
    } else {
        console.error('django.jQuery not found. Ensure admin scripts are loaded properly.');
    }
});
