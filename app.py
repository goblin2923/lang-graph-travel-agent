# pylint: disable = invalid-name
import os
import uuid

import streamlit as st
from langchain_core.messages import HumanMessage

from agents.agent import Agent


def populate_envs(sender_email, receiver_email, subject):
    os.environ['FROM_EMAIL'] = sender_email
    os.environ['TO_EMAIL'] = receiver_email
    os.environ['EMAIL_SUBJECT'] = subject


def send_email(sender_email, receiver_email, subject, thread_id):
    try:
        populate_envs(sender_email, receiver_email, subject)
        config = {'configurable': {'thread_id': thread_id}}
        st.session_state.agent.graph.invoke(None, config=config)
        st.success('Email sent successfully!')
        # Clear session state
        for key in ['travel_info', 'thread_id']:
            st.session_state.pop(key, None)
    except Exception as e:
        st.error(f'Error sending email: {e}')


def initialize_agent():
    if 'agent' not in st.session_state:
        st.session_state.agent = Agent()


def render_custom_css():
    st.markdown(
        '''
        <style>
        .main-title {
            font-size: 2.5em;
            color: #fff;
            text-align: center;
            margin-bottom: 0.5em;
            font-weight: bold;
        }
        .sub-title {
            font-size: 1.2em;
            color: #fff;
            text-align: center;
            margin-bottom: 0.5em;
        }
        .center-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
        }
        .query-box {
            width: 80%;
            max-width: 600px;
            margin-top: 0.5em;
            margin-bottom: 1em;
        }
        .query-container {
            width: 80%;
            max-width: 600px;
            margin: 0 auto;
        }
        </style>
        ''', unsafe_allow_html=True)


def render_ui():
    st.markdown('<div class="center-container">', unsafe_allow_html=True)
    st.markdown('<div class="main-title">✈️🌍 AI Travel Agent 🏨🗺️</div>', unsafe_allow_html=True)
    st.markdown('<div class="query-container">', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Enter your travel query and get flight and hotel information:</div>', unsafe_allow_html=True)
    user_input = st.text_area(
        'Travel Query',
        height=200,
        key='query',
        placeholder='Type your travel query here...',
    )


    return user_input


def process_query(user_input):
    if user_input:
        try:
            thread_id = str(uuid.uuid4())
            st.session_state.thread_id = thread_id

            messages = [HumanMessage(content=user_input)]
            config = {'configurable': {'thread_id': thread_id}}

            result = st.session_state.agent.graph.invoke({'messages': messages}, config=config)

            st.subheader('Travel Information')
            st.write(result['messages'][-1].content)

            st.session_state.travel_info = result['messages'][-1].content

        except Exception as e:
            st.error(f'Error: {e}')
    else:
        st.error('Please enter a travel query.')


def main():
    initialize_agent()
    render_custom_css()
    user_input = render_ui()

    if st.button('Get Travel Information'):
        process_query(user_input)



if __name__ == '__main__':
    main()
