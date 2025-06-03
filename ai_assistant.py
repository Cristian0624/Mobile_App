from kivy.properties import StringProperty, BooleanProperty
from kivy.event import EventDispatcher
from kivy.clock import Clock
import threading
import time
import random
import json

class AIAssistant(EventDispatcher):
    """A simplified AI assistant that doesn't require external dependencies"""
    response_text = StringProperty('')
    recognized_text = StringProperty('')
    is_listening = BooleanProperty(False)
    is_speaking = BooleanProperty(False)
    is_processing = BooleanProperty(False)
    
    # Event fired when a reminder should be created
    # Format: {'medication': str, 'dosage': str, 'frequency': str, 'duration': int or None}
    create_reminder_event = StringProperty('')
    
    def __init__(self, *args, **kwargs):
        super(AIAssistant, self).__init__(*args, **kwargs)
        self.responses = {
            'greeting': [
                "Hello! I'm your health and wellness assistant. How can I help you today?",
                "Hi there! I can assist with medication management, nutrition, exercise, and overall wellness. What do you need help with?",
                "Welcome! I'm here to help you maintain a healthy lifestyle. What can I assist you with?"
            ],
            'vitamins': [
                "Vitamins are essential nutrients that support various bodily functions. Common ones include Vitamin C for immune support, Vitamin D for bone health, and B vitamins for energy.",
                "When considering vitamins, it's important to get them primarily from a balanced diet. Foods like fruits, vegetables, whole grains, and lean proteins are great sources.",
                "If you're thinking about supplements, it's best to consult with a healthcare provider first to ensure you're getting the right ones for your needs."
            ],
            'exercise': [
                "A balanced exercise routine should include a mix of cardiovascular, strength, and flexibility training. Aim for at least 150 minutes of moderate activity per week.",
                "For beginners, start with low-impact activities like walking or swimming, then gradually increase intensity and duration.",
                "Remember to warm up before exercise and cool down afterward to prevent injuries. Listen to your body and don't push too hard too soon."
            ],
            'nutrition': [
                "A balanced diet includes a variety of foods from all food groups. Focus on whole foods like fruits, vegetables, lean proteins, and whole grains.",
                "For weight management, pay attention to portion sizes and try to maintain a calorie deficit while still getting all necessary nutrients.",
                "Hydration is crucial for overall health. Aim for about 8 glasses of water per day, more if you're active or in hot weather."
            ],
            'wellness': [
                "Stress management is key to overall wellness. Techniques like meditation, deep breathing, and regular exercise can help reduce stress levels.",
                "Getting enough sleep is essential for health. Most adults need 7-9 hours per night. Establish a consistent sleep schedule and create a relaxing bedtime routine.",
                "Regular check-ups with healthcare providers are important for preventive care and maintaining good health."
            ],
            'reminder': [
                "I can help you set up reminders for your medications, vitamins, or other health-related tasks. Just let me know what you'd like to be reminded about and when.",
                "For medication reminders, it's important to specify the exact time and frequency. This helps ensure you take your medications consistently.",
                "I can also set reminders for your exercise routine or other health goals. What would you like me to help you remember?"
            ],
            'fallback': [
                "I'm here to help with health and wellness topics! I can assist with medication management, nutrition, exercise, and general wellness. What would you like to know about?",
                "I can help you set up reminders for medications, vitamins, or other health-related tasks. Just let me know what you'd like to be reminded about and when.",
                "For specific medical advice, please consult your healthcare provider. I'm here to provide general health and wellness information."
            ]
        }
    
    def process_text_input(self, user_input):
        """Process text input and generate a response"""
        self.is_processing = True
        self.recognized_text = user_input
        
        # Process in a separate thread to simulate AI thinking
        threading.Thread(target=self._simulate_processing, args=(user_input,)).start()
    
    def _simulate_processing(self, user_input):
        """Simulate AI processing with a delay"""
        # Simulate processing time
        time.sleep(1.5)
        
        # Generate response based on keywords in user input
        response = self._generate_response(user_input.lower())
        
        # Update response on the main thread
        Clock.schedule_once(lambda dt: self._update_response(response), 0)
    
    def _generate_response(self, user_input):
        """Generate a response based on keywords in the user input"""
        # Check if this is a request to create a reminder
        if self._check_for_reminder_request(user_input):
            return self._handle_reminder_request(user_input)
            
        # Handle health and wellness queries
        if any(word in user_input for word in ['hello', 'hi', 'hey', 'greetings']):
            category = 'greeting'
        elif any(word in user_input for word in ['vitamin', 'supplement', 'nutrition']):
            category = 'vitamins'
        elif any(word in user_input for word in ['exercise', 'workout', 'fitness', 'training']):
            category = 'exercise'
        elif any(word in user_input for word in ['diet', 'meal', 'nutrition', 'food']):
            category = 'nutrition'
        elif any(word in user_input for word in ['stress', 'sleep', 'wellness', 'health']):
            category = 'wellness'
        elif any(word in user_input for word in ['medicine', 'medication', 'pill']):
            category = 'reminder'
        else:
            category = 'fallback'
        
        # Return a random response from the selected category
        return random.choice(self.responses[category])
        
    def _check_for_reminder_request(self, user_input):
        """Check if the user is requesting to create a reminder"""
        # Pattern 1: Direct request to create/set/add a reminder
        reminder_phrases = [
            'create reminder', 'set reminder', 'add reminder', 'create a reminder',
            'set a reminder', 'add a reminder', 'make reminder', 'make a reminder',
            'remind me to take', 'set an alarm', 'create an alarm',
            'remind me about', 'schedule', 'set a timer'
        ]
        pattern1 = any(phrase in user_input for phrase in reminder_phrases)
        
        # Pattern 2: Mentions reminder concept with any health-related item
        reminder_words = ['remind', 'reminder', 'schedule', 'alarm', 'timer']
        health_items = ['medicine', 'medication', 'pill', 'vitamin', 'supplement', 'exercise', 'workout', 'meal']
        has_reminder_word = any(word in user_input for word in reminder_words)
        has_health_item = any(word in user_input for word in health_items)
        has_medication_word = any(word in user_input for word in [
            'medicine', 'medication', 'antibiotic', 'pill', 'drug', 'dose', 'prescription',
            'amoxicillin', 'penicillin', 'ciprofloxacin', 'azithromycin', 'doxycycline'
        ])
        pattern2 = has_reminder_word and has_medication_word
        
        return pattern1 or pattern2
    
    def _handle_reminder_request(self, user_input):
        """Handle a request to create a medication reminder"""
        # Extract medication information from the user input
        medication_info = self._extract_medication_info(user_input)
        print(f"Extracted medication info: {medication_info}")
        
        # Check if we have a medication name
        if not medication_info.get('medication'):
            return "I'd be happy to create a reminder for you. What medication do you need to be reminded about?"
            
        # Check if we have dosage information
        if not medication_info.get('dosage'):
            return f"Sure, I'll create a reminder for {medication_info['medication']}. What's the dosage you need to take?"
            
        # Check if we have frequency information
        if not medication_info.get('frequency'):
            return f"I'll set up a reminder for {medication_info['medication']} {medication_info['dosage']}. How often do you need to take it?"
        
        # We have all the required information, create the reminder
        # Convert to JSON string to pass through the property
        try:
            # Generate a direct reminder creation message
            reminder_message = f"Creating reminder for {medication_info['medication']} {medication_info['dosage']} to be taken {medication_info['frequency']}"
            if medication_info.get('duration'):
                reminder_message += f" for {medication_info['duration']} days"
            
            print(f"Reminder message: {reminder_message}")
            
            # Convert to JSON string and set the property
            reminder_json = json.dumps(medication_info)
            
            # Use Clock to set the property on the main thread to avoid threading issues
            def set_property(dt):
                print(f"Setting create_reminder_event to: {reminder_json}")
                self.create_reminder_event = reminder_json
                print(f"Property set: {self.create_reminder_event}")
                
            Clock.schedule_once(set_property, 0.1)
        except Exception as e:
            print(f"Error creating reminder json: {e}")
        
        # Generate a confirmation response
        frequency = medication_info['frequency']
        medication = medication_info['medication']
        dosage = medication_info['dosage']
        duration_text = ""
        if medication_info.get('duration'):
            duration_text = f" for {medication_info['duration']} days"
        
        return f"I've created a reminder for you to take {dosage} of {medication} {frequency}{duration_text}. You can view and edit this reminder in the Reminders section."
    
    def _extract_medication_info(self, user_input):
        """Extract medication information from user input"""
        # Initialize with empty values
        info = {
            'medication': None,
            'dosage': None,
            'frequency': None,
            'duration': None
        }
        
        # Common antibiotics to check for
        common_antibiotics = [
            'amoxicillin', 'penicillin', 'azithromycin', 'ciprofloxacin', 'doxycycline',
            'metronidazole', 'clindamycin', 'erythromycin', 'cephalexin', 'sulfamethoxazole',
            'tetracycline', 'levofloxacin', 'clarithromycin', 'vancomycin', 'minocycline',
            'antibiotic', 'medication', 'medicine', 'pill', 'prescription'
        ]
        
        # Check for medication names
        words = user_input.lower().split()
        for antibiotic in common_antibiotics:
            if antibiotic in user_input.lower():
                info['medication'] = antibiotic.title()
                break
        
        # Check for dosage (look for patterns like 500mg, 250 mg, etc.)
        import re
        dosage_patterns = [
            r'\b(\d+)\s*mg\b',  # 500mg or 500 mg
            r'\b(\d+)\s*ml\b',  # 5ml or 5 ml
            r'\b(\d+)\s*tablet(s)?\b',  # 2 tablets
            r'\b(\d+)\s*pill(s)?\b',  # 2 pills
            r'\b(\d+)\s*capsule(s)?\b',  # 1 capsule
        ]
        
        for pattern in dosage_patterns:
            match = re.search(pattern, user_input.lower())
            if match:
                if 'mg' in pattern:
                    info['dosage'] = match.group(1) + ' mg'
                elif 'ml' in pattern:
                    info['dosage'] = match.group(1) + ' ml'
                elif 'tablet' in pattern or 'pill' in pattern or 'capsule' in pattern:
                    info['dosage'] = match.group(1) + ' ' + match.group(0).split()[1]
                break
        
        # Check for frequency
        frequency_phrases = {
            'once daily': ['once daily', 'once a day', 'daily', 'every day', 'each day'],
            'twice daily': ['twice daily', 'twice a day', 'two times a day', 'bid', '2 times daily'],
            'three times daily': ['three times daily', 'three times a day', 'tid', '3 times daily'],
            'four times daily': ['four times daily', 'four times a day', 'qid', '4 times daily'],
            'every 6 hours': ['every 6 hours', 'every six hours', 'q6h'],
            'every 8 hours': ['every 8 hours', 'every eight hours', 'q8h'],
            'every 12 hours': ['every 12 hours', 'every twelve hours', 'q12h']
        }
        
        for freq, phrases in frequency_phrases.items():
            if any(phrase in user_input.lower() for phrase in phrases):
                info['frequency'] = freq
                break
        
        # Check for duration (look for patterns like 7 days, 10 days, etc.)
        duration_pattern = r'\b(\d+)\s*days?\b'  # 7 days or 7 day
        match = re.search(duration_pattern, user_input.lower())
        if match:
            info['duration'] = int(match.group(1))
        
        return info
    
    def _update_response(self, text):
        """Update response text and set is_processing to False"""
        self.response_text = text
        self.is_processing = False
    
    def ask(self, question):
        """Process a question and return a response"""
        # Process the question using existing method
        self.process_text_input(question)
        
        # Wait for processing to complete (simple synchronous approach)
        timeout = 3  # seconds
        start_time = time.time()
        while self.is_processing and time.time() - start_time < timeout:
            time.sleep(0.1)
        
        # Return the generated response
        return self.response_text
    
    def start_voice_input(self):
        """Simulate voice input (without actual speech recognition)"""
        self.is_listening = True
        
        # Simulate listening with a delay
        threading.Thread(target=self._simulate_listening).start()
    
    def _simulate_listening(self):
        """Simulate listening process"""
        # Pretend to listen for 2 seconds
        time.sleep(2)
        
        # Simulate microphone not detecting speech
        if random.random() < 0.2:  # 20% chance of not detecting speech
            self.response_text = "I didn't hear anything. Please try again or type your message."
        else:
            # Simulate recognized text
            simulated_inputs = [
                "How do antibiotics work?",
                "When should I take my medication?",
                "What are common side effects?",
                "Can you set a reminder for me?",
                "What is amoxicillin used for?"
            ]
            self.recognized_text = random.choice(simulated_inputs)
        
        # Update state on the main thread
        Clock.schedule_once(lambda dt: setattr(self, 'is_listening', False), 0)
