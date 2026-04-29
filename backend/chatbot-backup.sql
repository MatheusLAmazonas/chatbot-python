--
-- PostgreSQL database dump
--

\restrict ihhDUhL2XsJKptJMIJOsvLvPmj26XqZcqYvRMTPpn3p3Xp8W2VxXPzcb1FiUNlq

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

-- Started on 2026-04-29 20:38:42

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 220 (class 1259 OID 16448)
-- Name: usuarios_chatbot; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios_chatbot (
    id integer NOT NULL,
    username character varying(80) NOT NULL,
    senha_hash character varying(255) NOT NULL
);


ALTER TABLE public.usuarios_chatbot OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16447)
-- Name: usuarios_chatbot_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_chatbot_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_chatbot_id_seq OWNER TO postgres;

--
-- TOC entry 5016 (class 0 OID 0)
-- Dependencies: 219
-- Name: usuarios_chatbot_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_chatbot_id_seq OWNED BY public.usuarios_chatbot.id;


--
-- TOC entry 4856 (class 2604 OID 16451)
-- Name: usuarios_chatbot id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios_chatbot ALTER COLUMN id SET DEFAULT nextval('public.usuarios_chatbot_id_seq'::regclass);


--
-- TOC entry 5010 (class 0 OID 16448)
-- Dependencies: 220
-- Data for Name: usuarios_chatbot; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios_chatbot (id, username, senha_hash) FROM stdin;
3	admin	$2b$12$flrfLOvc0l0yi3D8JZByguWlLKYx/mgwU3fI8GiqOjVNGQD4rU7pq
5	minotauro	$2b$12$dTJ6sjL/ch73VrnR7DeWAu.X4wuLkpeaQHTlJVL4LNozHqk8mWCm.
1	ale	$2b$12$WDHhOoZeJ75mJQR5t9CEU.A6F9/QseCKKV0CuIFCEWxnPjRld/X8.
\.


--
-- TOC entry 5017 (class 0 OID 0)
-- Dependencies: 219
-- Name: usuarios_chatbot_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_chatbot_id_seq', 5, true);


--
-- TOC entry 4859 (class 2606 OID 16456)
-- Name: usuarios_chatbot usuarios_chatbot_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios_chatbot
    ADD CONSTRAINT usuarios_chatbot_pkey PRIMARY KEY (id);


--
-- TOC entry 4861 (class 2606 OID 16458)
-- Name: usuarios_chatbot usuarios_chatbot_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios_chatbot
    ADD CONSTRAINT usuarios_chatbot_username_key UNIQUE (username);


--
-- TOC entry 4857 (class 1259 OID 16459)
-- Name: ix_usuarios_chatbot_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_usuarios_chatbot_id ON public.usuarios_chatbot USING btree (id);


-- Completed on 2026-04-29 20:38:43

--
-- PostgreSQL database dump complete
--

\unrestrict ihhDUhL2XsJKptJMIJOsvLvPmj26XqZcqYvRMTPpn3p3Xp8W2VxXPzcb1FiUNlq

