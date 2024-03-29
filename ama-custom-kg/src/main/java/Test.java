import org.apache.jena.rdf.model.*;

import java.util.*;

public class Test {
    public static String AMA_BASE = "http://www.w3.org/2001/ama/sjsu";

    // create an empty Model
    public static Model MODEL = ModelFactory
            .createDefaultModel();
            //.setNsPrefix("", AMA_BASE);

    public static Property FIRST_NAME_PROP = MODEL.createProperty(AMA_BASE + "#firstName");
    public static Property LAST_NAME_PROP = MODEL.createProperty(AMA_BASE + "#lastName");
    public static Property FULL_NAME_PROP = MODEL.createProperty(AMA_BASE + "#fullName");
    public static Property NAME_PROP = MODEL.createProperty(AMA_BASE + "#name");
    public static Property TYPE_PROP = MODEL.createProperty(AMA_BASE + "#type");
    public static Property FIELD_PROP = MODEL.createProperty(AMA_BASE + "#field");
    public static Property DEPARTMENT_NAME_PROP = MODEL.createProperty(AMA_BASE + "#department");
    public static Property TEACHES_PROP = MODEL.createProperty(AMA_BASE + "#teaches");
    public static Property NUMBER_PROP = MODEL.createProperty(AMA_BASE + "#number");
    public static Property SJSU_ID_PROP = MODEL.createProperty(AMA_BASE + "#sjsuId");
    public static Property EMAIL_PROP = MODEL.createProperty(AMA_BASE + "#email");
    public static Property TUITION_FEES_PROP = MODEL.createProperty(AMA_BASE + "#tuitionFees");
    public static Property CONTACT_NUMBER_PROP = MODEL.createProperty(AMA_BASE + "#contactNumber");
    public static Property CRITERIA_PROP = MODEL.createProperty(AMA_BASE + "#criteria");
    public static Property APPLICATION_FEES_PROP = MODEL.createProperty(AMA_BASE + "#applicationFees");
    public static Property PROPERTY_PROP = MODEL.createProperty(AMA_BASE + "#property");
    public static Property HAS_ALIAS = MODEL.createProperty(AMA_BASE + "#hasAlias");
    public static Property PRE_REQUISITES_PROP = MODEL.createProperty(AMA_BASE + "#preRequisites");
    public static Property STUDENT_LEVEL_PROP = MODEL.createProperty(AMA_BASE + "#studentLevel");
    public static Property SCHOOL_PROP = MODEL.createProperty(AMA_BASE + "#school");
    public static Property INFO_PROP = MODEL.createProperty(AMA_BASE + "#info");


    public static void printRDFObject() {
        StmtIterator iter = MODEL.listStatements();

        // print out the predicate, subject and object of each statement
        while (iter.hasNext()) {
            Statement stmt      = iter.nextStatement();  // get next statement
            Resource  subject   = stmt.getSubject();     // get the subject
            Property  predicate = stmt.getPredicate();   // get the predicate
            RDFNode   object    = stmt.getObject();      // get the object

            System.out.print("<" + subject.toString() + ">");
            System.out.print(" <" + predicate.toString() + ">");
            if (object instanceof Resource) {
                System.out.print(" <" + object.toString() + ">");
            } else {
                // object is a literal
                System.out.print(" \"" + object.toString() + "\"");
            }

            System.out.println(" .");
        }
    }

    public static  Map<String, List<String>> aliases  = new HashMap<String, List<String>>() {{
        put("email", new ArrayList<>(
                Arrays.asList("email", "email id", "email address", "contact")));
        put("tuition_fees", new ArrayList<>(
                Arrays.asList("tuition fees", "tuition", "fees", "fee")));
        put("contact_number", new ArrayList<>(
                Arrays.asList("reach", "number", "phone number", "contact number", "contact")));
        put("application_fees", new ArrayList<>(
                Arrays.asList("application fees", "application fee")));
        put("criteria", new ArrayList<>(
                Arrays.asList("criterion", "criteria")));
        put("pre_requisites", new ArrayList<>(
                Arrays.asList("pre requisites", "pre - requisite", "pre-requisites", "pre req", "pre reqs", "requirements", "requirement")));
    }};

    public static  Map<String, Property> aliasMap  = new HashMap<String, Property>() {{
        put("email", EMAIL_PROP);
        put("tuition_fees", TUITION_FEES_PROP);
        put("pre_requisites", PRE_REQUISITES_PROP);
        put("contact_number", CONTACT_NUMBER_PROP);
        put("application_fees", APPLICATION_FEES_PROP);
        put("criteria", CRITERIA_PROP);
    }};

    public static  Map<String, Property> departmentMap  = new HashMap<String, Property>() {{
        put("name", NAME_PROP);
        put("sjsuId", SJSU_ID_PROP);
        put("type", TYPE_PROP);
        put("contact_number", CONTACT_NUMBER_PROP);
        put("application_fees", APPLICATION_FEES_PROP);
    }};

    public static  Map<String, Property> scholarshipMap  = new HashMap<String, Property>() {{
        put("name", NAME_PROP);
        put("sjsuId", SJSU_ID_PROP);
        put("type", TYPE_PROP);
        put("studentLevel", STUDENT_LEVEL_PROP);
        put("school", SCHOOL_PROP);
    }};

    public static  Map<String, Property> serviceMap  = new HashMap<String, Property>() {{
        put("name", NAME_PROP);
        put("sjsuId", SJSU_ID_PROP);
        put("type", TYPE_PROP);
        put("info", INFO_PROP);
    }};


    public static  Map<String, Property> semesterMap  = new HashMap<String, Property>() {{
        put("name", NAME_PROP);
        put("sjsuId", SJSU_ID_PROP);
        put("tuition_fees", TUITION_FEES_PROP);
    }};

    public static  Map<String, Property> majorMap  = new HashMap<String, Property>() {{
        put("name", NAME_PROP);
        put("sjsuId", SJSU_ID_PROP);
        put("criteria", CRITERIA_PROP);
        put("type", TYPE_PROP);
        put("email", EMAIL_PROP);
    }};

    public static  Map<String, Property> courseMap = new HashMap<String, Property>() {{
        put("name", NAME_PROP);
        put("sjsuId", SJSU_ID_PROP);
        put("number", NUMBER_PROP);
        put("department", DEPARTMENT_NAME_PROP);
        put("type", TYPE_PROP);
        put("field", FIELD_PROP);
        put("pre_requisites", PRE_REQUISITES_PROP);
    }};

    public static  Map<String, Property> personelMap = new HashMap<String, Property>() {{
        put("firstName", FIRST_NAME_PROP);
        put("lastName", LAST_NAME_PROP);
        put("name", NAME_PROP);
        put("type", TYPE_PROP);
        put("department", DEPARTMENT_NAME_PROP);
        put("course", TEACHES_PROP);
        put("sjsuId", SJSU_ID_PROP);
        put("email", EMAIL_PROP);
    }};

    public static void main(String[] args) {
        String personURI    = "DanHarkey_12345";
        String givenName    = "Dan";
        String familyName   = "Harkey";
        String fullName     = givenName + " " + familyName;


        // create the resource
        //   and add the properties cascading style
        Resource danHarkey
                = MODEL.createResource(AMA_BASE + "/" + personURI)
                .addProperty(FULL_NAME_PROP, fullName)
                .addProperty(FIRST_NAME_PROP, givenName)
                .addProperty(LAST_NAME_PROP, familyName);

        Resource vg
                = MODEL.createResource(AMA_BASE + "/" + "VinodhGopinath_789")
                .addProperty(FULL_NAME_PROP, "Vinodh Gopinath")
                .addProperty(FIRST_NAME_PROP, "Vinodh")
                .addProperty(FIRST_NAME_PROP, "Name2")
                .addProperty(LAST_NAME_PROP, "Gopinath");

//                .addProperty(NAME_PROP,
//                        MODEL.createResource()
//                                .addProperty(FIRST_NAME_PROP, givenName)
//                                .addProperty(LAST_NAME_PROP, familyName));

        // list the statements in the Model
        StmtIterator iter = MODEL.listStatements();

        // print out the predicate, subject and object of each statement
        while (iter.hasNext()) {
            Statement stmt      = iter.nextStatement();  // get next statement
            Resource  subject   = stmt.getSubject();     // get the subject
            Property  predicate = stmt.getPredicate();   // get the predicate
            RDFNode   object    = stmt.getObject();      // get the object

            System.out.print("<" + subject.toString() + ">");
            System.out.print(" <" + predicate.toString() + ">");
            if (object instanceof Resource) {
                System.out.print("<" + object.toString() + ">");
            } else {
                // object is a literal
                System.out.print(" \"" + object.toString() + "\"");
            }

            System.out.println(" .");
        }

//        StmtIterator stmtiter = MODEL.listStatements(
//                new SimpleSelector(null, FULL_NAME_PROP, (RDFNode) null) {
//                    public boolean selects(Statement s)
//                    {return s.getString().endsWith("Smith");}
//                });
//
//        if (stmtiter.hasNext()) {
//            System.out.println("The database contains vcards for:");
//            while (stmtiter.hasNext()) {
//                System.out.println("  " + stmtiter.nextStatement().getObject());
//            }
//        } else {
//            System.out.println("No vcards were found in the database");
//        }
    }
}