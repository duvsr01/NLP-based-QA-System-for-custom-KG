import org.apache.jena.rdf.model.*;

import java.util.HashMap;
import java.util.Map;

public class Test {
    public static String AMA_BASE = "http://www.w3.org/2001/ama/sjsu";

    // create an empty Model
    public static Model MODEL = ModelFactory
            .createDefaultModel();
            //.setNsPrefix("", AMA_BASE);

    private static Property FIRST_NAME_PROP = MODEL.createProperty(AMA_BASE + "#firstName");
    private static Property LAST_NAME_PROP = MODEL.createProperty(AMA_BASE + "#lastName");
    private static Property FULL_NAME_PROP = MODEL.createProperty(AMA_BASE + "#fullName");
    private static Property NAME_PROP = MODEL.createProperty(AMA_BASE + "#name");
    private static Property TYPE_PROP = MODEL.createProperty(AMA_BASE + "#type");
    private static Property DEPARTMENT_NAME_PROP = MODEL.createProperty(AMA_BASE + "#department");
    private static Property SJSU_ID_PROP = MODEL.createProperty(AMA_BASE + "#sjsuId");

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
                System.out.print("<" + object.toString() + ">");
            } else {
                // object is a literal
                System.out.print(" \"" + object.toString() + "\"");
            }

            System.out.println(" .");
        }
    }

    public static  Map<String, Property> personelMap  = new HashMap<String, Property>() {{
        put("firstName", FIRST_NAME_PROP);
        put("lastName", LAST_NAME_PROP);
        put("fullName", FULL_NAME_PROP);
        put("type", TYPE_PROP);
        put("department", DEPARTMENT_NAME_PROP);
        put("sjsuId", SJSU_ID_PROP);
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