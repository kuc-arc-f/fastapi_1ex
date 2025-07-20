CREATE TABLE public.items (
    id bigint NOT NULL,
    title character varying,
    content text,
    created_at timestamp(6) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(6) without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.items OWNER TO postgres;