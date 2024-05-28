--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: access_level_enum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.access_level_enum AS ENUM (
    'read_only',
    'write',
    'admin'
);


ALTER TYPE public.access_level_enum OWNER TO postgres;

--
-- Name: transform; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.transform AS ENUM (
    'read_only',
    'write',
    'admin'
);


ALTER TYPE public.transform OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: calcs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.calcs (
    calc_id integer NOT NULL,
    house_price character varying,
    down_payment character varying,
    bond_price character varying,
    bank_name character varying,
    principal_value character varying,
    capital_loss character varying,
    user_id integer
);


ALTER TABLE public.calcs OWNER TO postgres;

--
-- Name: calcs_calc_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.calcs_calc_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.calcs_calc_id_seq OWNER TO postgres;

--
-- Name: calcs_calc_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.calcs_calc_id_seq OWNED BY public.calcs.calc_id;


--
-- Name: sharedCalcsWithAll; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."sharedCalcsWithAll" (
    calc_id integer NOT NULL,
    user_id integer NOT NULL,
    access_level public.access_level_enum
);


ALTER TABLE public."sharedCalcsWithAll" OWNER TO postgres;

--
-- Name: sharedCalcsWithFew; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."sharedCalcsWithFew" (
    shared_id integer NOT NULL,
    calc_id integer,
    user_id integer,
    access_level public.access_level_enum
);


ALTER TABLE public."sharedCalcsWithFew" OWNER TO postgres;

--
-- Name: sharedCalcsWithFew_shared_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."sharedCalcsWithFew_shared_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."sharedCalcsWithFew_shared_id_seq" OWNER TO postgres;

--
-- Name: sharedCalcsWithFew_shared_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."sharedCalcsWithFew_shared_id_seq" OWNED BY public."sharedCalcsWithFew".shared_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    email character varying NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: calcs calc_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calcs ALTER COLUMN calc_id SET DEFAULT nextval('public.calcs_calc_id_seq'::regclass);


--
-- Name: sharedCalcsWithFew shared_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."sharedCalcsWithFew" ALTER COLUMN shared_id SET DEFAULT nextval('public."sharedCalcsWithFew_shared_id_seq"'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: calcs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.calcs (calc_id, house_price, down_payment, bond_price, bank_name, principal_value, capital_loss, user_id) FROM stdin;
1	500000	100000	97	Totalkredit	442105	22105	1
2	800000	160000	94	RealkreditDanmark	715217	57217	1
3	1000000	50000	99	RealkreditDanmark	997938	29938	2
4	750000	150000	95	RealkreditDanmark	664516	46516	2
\.


--
-- Data for Name: sharedCalcsWithAll; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."sharedCalcsWithAll" (calc_id, user_id, access_level) FROM stdin;
1	2	read_only
2	2	write
3	1	write
\.


--
-- Data for Name: sharedCalcsWithFew; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."sharedCalcsWithFew" (shared_id, calc_id, user_id, access_level) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, email) FROM stdin;
1	CMnlCQ850rbQnmKoc5TP13qfQ5aO+TzuWXHffhS3j8uWP8HwboIOdLMOVbgQrps7
2	eg+pGeTjOxszmsEeDMOiABr4t0rLDreKwq7hLt1Laz2VbxrxrypmcqUw2mkKWVs=
\.


--
-- Name: calcs_calc_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.calcs_calc_id_seq', 4, true);


--
-- Name: sharedCalcsWithFew_shared_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."sharedCalcsWithFew_shared_id_seq"', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 2, true);


--
-- Name: calcs calcs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calcs
    ADD CONSTRAINT calcs_pkey PRIMARY KEY (calc_id);


--
-- Name: sharedCalcsWithAll sharedCalcsWithAll_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."sharedCalcsWithAll"
    ADD CONSTRAINT "sharedCalcsWithAll_pkey" PRIMARY KEY (calc_id, user_id);


--
-- Name: sharedCalcsWithFew sharedCalcsWithFew_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."sharedCalcsWithFew"
    ADD CONSTRAINT "sharedCalcsWithFew_pkey" PRIMARY KEY (shared_id);


--
-- Name: sharedCalcsWithFew unique_calc_user; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."sharedCalcsWithFew"
    ADD CONSTRAINT unique_calc_user UNIQUE (calc_id, user_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: calcs calcs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.calcs
    ADD CONSTRAINT calcs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: sharedCalcsWithAll sharedCalcsWithAll_calc_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."sharedCalcsWithAll"
    ADD CONSTRAINT "sharedCalcsWithAll_calc_id_fkey" FOREIGN KEY (calc_id) REFERENCES public.calcs(calc_id) ON DELETE CASCADE;


--
-- Name: sharedCalcsWithAll sharedCalcsWithAll_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."sharedCalcsWithAll"
    ADD CONSTRAINT "sharedCalcsWithAll_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: sharedCalcsWithFew sharedCalcsWithFew_calc_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."sharedCalcsWithFew"
    ADD CONSTRAINT "sharedCalcsWithFew_calc_id_fkey" FOREIGN KEY (calc_id) REFERENCES public.calcs(calc_id) ON DELETE CASCADE;


--
-- Name: sharedCalcsWithFew sharedCalcsWithFew_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."sharedCalcsWithFew"
    ADD CONSTRAINT "sharedCalcsWithFew_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

