(function() {
    // Function to send a tracking event to your backend API
    const trackEvent = (eventType, eventData) => {
      fetch('/activity_tracker', {  // Replace this with your actual Flask endpoint
        method: "POST",                      // Use POST to send event data
        headers: { "Content-Type": "application/json" }, // Set content type
        body: JSON.stringify({              // Prepare the event data as JSON
          eventType,                        // e.g., "button_click", "page_view"
          eventData,                        // any extra info, like button name
          timestamp: new Date().toISOString(), // Capture the current time
          page: window.location.pathname    // Track which page the event happened on
        })
      });
    };
  
    // Function to initialize tracking with a config object
    const initTracking = (config) => {
      // Loop through all defined events in the config (Script i created in the base template)
      config.events.forEach(evt => {
        const elements = document.querySelectorAll(evt.selector); // Select elements matching the given CSS selector
        elements.forEach(el => {
          // Attach event listener (e.g., 'click') to each element
          el.addEventListener(evt.on, () => {
            trackEvent(evt.name, evt.meta || {}); // Send the event when triggered
          });
        });
      });
  
      // If page views are enabled, track when the page loads
      if (config.trackPageView) {
        trackEvent("page_view", {}); // Send a "page_view" event with no extra data
      }
    };
  
    // Make the init function globally accessible so you can call it in your page
    window.initUserTracker = initTracking;
  })();