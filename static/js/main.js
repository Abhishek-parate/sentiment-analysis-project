/**
 * SentimentAI - Main JavaScript functionality
 */

// DOM ready
document.addEventListener('DOMContentLoaded', function() {
    
    // Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Flash message close buttons
    const closeButtons = document.querySelectorAll('.close-alert');
    if (closeButtons) {
        closeButtons.forEach(button => {
            button.addEventListener('click', function() {
                this.parentElement.remove();
            });
        });
    }

    // Sentiment Analysis - Sample Text button
    const sampleTextButton = document.getElementById('sample-text');
    const textArea = document.getElementById('text');
    
    if (sampleTextButton && textArea) {
        // Sample text examples
        const sampleTexts = [
            "I absolutely loved the new product! It exceeded all my expectations and made my life so much easier.",
            "The customer service was terrible. I waited for hours and nobody helped me resolve my issue.",
            "The conference starts at 9 AM tomorrow. Please bring your laptop and presentation materials.",
            "While the design was beautiful, the functionality was disappointing and didn't work as advertised.",
            "I'm not sure how I feel about the new policy changes. They might be good in some ways but concerning in others."
        ];
        
        sampleTextButton.addEventListener('click', function() {
            const randomIndex = Math.floor(Math.random() * sampleTexts.length);
            textArea.value = sampleTexts[randomIndex];
        });
    }

    // API Demo - if on the test page
    const apiDemo = document.getElementById('api-demo');
    if (apiDemo) {
        apiDemo.addEventListener('click', async function() {
            const demoText = textArea.value || "This is a demo of the SentimentAI API. It works great!";
            const resultDiv = document.getElementById('api-result');
            
            if (resultDiv) {
                resultDiv.innerHTML = '<div class="animate-pulse p-4 bg-gray-100 rounded-md">Analyzing...</div>';
                
                try {
                    const response = await fetch('/api/analyze', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ text: demoText }),
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        // Get emoji based on sentiment
                        let emoji = '😐';
                        if (data.sentiment === 'positive') emoji = '😊';
                        if (data.sentiment === 'negative') emoji = '😔';
                        
                        // Get color based on sentiment
                        let colorClass = 'bg-gray-100 border-gray-300';
                        if (data.sentiment === 'positive') colorClass = 'bg-green-50 border-green-200';
                        if (data.sentiment === 'negative') colorClass = 'bg-red-50 border-red-200';
                        
                        resultDiv.innerHTML = `
                            <div class="p-4 rounded-md border ${colorClass}">
                                <div class="flex items-center">
                                    <span class="text-2xl mr-2">${emoji}</span>
                                    <div>
                                        <div class="font-medium capitalize">${data.sentiment}</div>
                                        <div class="text-sm">Score: ${data.score.toFixed(2)}</div>
                                    </div>
                                </div>
                                <p class="mt-2">${data.explanation}</p>
                            </div>
                        `;
                    } else {
                        resultDiv.innerHTML = `
                            <div class="p-4 rounded-md bg-red-50 border border-red-200 text-red-800">
                                Error: ${data.error || 'Something went wrong'}
                            </div>
                        `;
                    }
                } catch (error) {
                    resultDiv.innerHTML = `
                        <div class="p-4 rounded-md bg-red-50 border border-red-200 text-red-800">
                            Error: ${error.message || 'Failed to connect to the API'}
                        </div>
                    `;
                }
            }
        });
    }

    // Password strength indicator for registration
    const passwordField = document.getElementById('password');
    const strengthIndicator = document.getElementById('password-strength');
    
    if (passwordField && strengthIndicator) {
        passwordField.addEventListener('input', function() {
            const password = this.value;
            let strength = 0;
            let message = '';
            
            // Length check
            if (password.length >= 8) {
                strength += 1;
            }
            
            // Contains lowercase letters
            if (password.match(/[a-z]/)) {
                strength += 1;
            }
            
            // Contains uppercase letters
            if (password.match(/[A-Z]/)) {
                strength += 1;
            }
            
            // Contains numbers
            if (password.match(/[0-9]/)) {
                strength += 1;
            }
            
            // Contains special characters
            if (password.match(/[^a-zA-Z0-9]/)) {
                strength += 1;
            }
            
            // Set the strength message and color
            let strengthClass = '';
            
            switch (strength) {
                case 0:
                case 1:
                    message = 'Weak';
                    strengthClass = 'bg-red-500';
                    break;
                case 2:
                case 3:
                    message = 'Moderate';
                    strengthClass = 'bg-yellow-500';
                    break;
                case 4:
                case 5:
                    message = 'Strong';
                    strengthClass = 'bg-green-500';
                    break;
                default:
                    message = '';
                    strengthClass = '';
            }
            
            // Update the strength indicator
            strengthIndicator.innerHTML = `
                <div class="mt-1 h-2 w-full bg-gray-200 rounded-full overflow-hidden">
                    <div class="${strengthClass} h-full" style="width: ${(strength / 5) * 100}%"></div>
                </div>
                <p class="text-xs mt-1 text-gray-600">Password strength: ${message}</p>
            `;
        });
    }
});