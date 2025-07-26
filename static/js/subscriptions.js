addEventListener('DOMContentLoaded', function() {
        // Function to check subscription status
        async function checkSubscriptionStatus() {
        console.log("Checking subscription status...");
            try {
                const response = await fetch('/check_subscriptions');
                const data = await response.json();

                if (!data.status) {
                    // If not subscribed, show the subscription modal
                    showSubscriptionModal();
                }
            } catch (error) {
                console.error('Error checking subscription status:', error);
            }
        }

        // Function to show the subscription modal
        function showSubscriptionModal() {
            const modal = document.createElement('div');
            modal.id = 'subscription-modal';
            modal.style.position = 'fixed';
            modal.style.top = '0';
            modal.style.left = '0';
            modal.style.width = '100%';
            modal.style.height = '100%';
            modal.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
            modal.style.display = 'flex';
            modal.style.justifyContent = 'center';
            modal.style.alignItems = 'center';
            modal.style.zIndex = '1000';

            modal.innerHTML = `
                <div class="notif-modal" style="background:rgba(255,255,255,0.5);backdrop-filter: blur(5px);border: 1px solid var(--main-color); padding:10px 20px; border-radius: 8px; text-align: center;">
                    <div style="display:flex;align-items:center;justify-content:center">
                        <img src="/static/icons/the-hustlers-time-logo.png" alt="Logo" style="width: 50px; height: auto;">
                    </div>
                    <h2>Subscribe for Notifications</h2>
                    <p style="font-size:12px;font-weight:500 !important;color:#222 !important">Get updates about jobs and other important notifications from The Hustlers Time.</p>
                    <button id="subscribe-btn" style="padding: 10px 20px; background: #006769; color: white; border: none; border-radius: 12px; cursor: pointer;">Subscribe</button>
                    <button id="close-modal-btn" style="font-weight:600;padding: 10px 20px; background: none; color: #777; border: none; border-radius: 4px; cursor: pointer; margin-left: 10px;">Dismiss</button>
                </div>
            `;

            document.body.appendChild(modal);

            // Add event listeners for buttons
            document.getElementById('subscribe-btn').addEventListener('click', subscribeUser);
            document.getElementById('close-modal-btn').addEventListener('click', () => {
                document.body.removeChild(modal);
            });
        }

        // Function to subscribe the user
        async function subscribeUser() {
            try {
                const registration = await navigator.serviceWorker.ready;
                const subscription = await registration.pushManager.subscribe({
                    userVisibleOnly: true,
                    applicationServerKey: "BKn-Jg1-Yh6ZXFAo7pM2CqifgkTgVp4Q8nxPVssc6L_ClABpjY8idgsFfqZRxT3Wmc496qRsTCB5JCFsC5eLTTA"
                });

                const response = await fetch('/subscribe', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(subscription)
                });

                const data = await response.json();
                if (data.status === 'subscribed') {
                    alert('You have successfully subscribed!');
                    document.getElementById('subscription-modal').remove();
                }
            } catch (error) {
                console.error('Error subscribing user:', error);
            }
        }

        // Check subscription status on page load
        window.onload = function() {
            setTimeout(checkSubscriptionStatus, 6000); // Wait for 3 seconds before running the function
        };

    async function checkAndUpdateSubscription() {
        try {
            const response = await fetch('/check_subscriptions');
            const data = await response.json();

            if (data.status) {
                // Update the subscription entry in the database
                const updateResponse = await fetch('/update_subscription', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ ip: data.ip })
                });

                const updateData = await updateResponse.json();
                if (updateData.status === 'updated') {
                    console.log('Subscription updated successfully.');
                } else {
                    console.error('Failed to update subscription.');
                }
            } else if (data.status === 'valid') {
                console.log('Subscription is still valid.');
            } else {
                console.log('No subscription found.');
            }
        } catch (error) {
            console.error('Error checking or updating subscription:', error);
        }
    }

    // Run the check and update function
    checkAndUpdateSubscription();

});