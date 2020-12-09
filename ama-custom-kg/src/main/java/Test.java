import org.apache.jena.rdf.model.*;

public class Test {
    private static String AMA_BASE = "http://www.w3.org/2001/ama/sjsu";

    // create an empty Model
    private static Model MODEL = ModelFactory
            .createDefaultModel();
            //.setNsPrefix("", AMA_BASE);

    private static Property FIRST_NAME_PROP = MODEL.createProperty(AMA_BASE + "#firstName");
    private static Property LAST_NAME_PROP = MODEL.createProperty(AMA_BASE + "#lastName");
    private static Property FULL_NAME_PROP = MODEL.createProperty(AMA_BASE + "#fullName");
    private static Property NAME_PROP = MODEL.createProperty(AMA_BASE + "#name");

    public static void main(String[] args) {
        String personURI    = "JohnSmith";
        String givenName    = "John";
        String familyName   = "Smith";
        String fullName     = givenName + " " + familyName;

        // create the resource
        //   and add the properties cascading style
        Resource johnSmith
                = MODEL.createResource(AMA_BASE + "/" + personURI)
                .addProperty(FULL_NAME_PROP, fullName)
                .addProperty(NAME_PROP,
                        MODEL.createResource()
                                .addProperty(FIRST_NAME_PROP, givenName)
                                .addProperty(LAST_NAME_PROP, familyName));

        // list the statements in the Model
        StmtIterator iter = MODEL.listStatements();

        // print out the predicate, subject and object of each statement
        while (iter.hasNext()) {
            Statement stmt      = iter.nextStatement();  // get next statement
            Resource  subject   = stmt.getSubject();     // get the subject
            Property  predicate = stmt.getPredicate();   // get the predicate
            RDFNode   object    = stmt.getObject();      // get the object

            System.out.print(subject.toString());
            System.out.print(" " + predicate.toString() + " ");
            if (object instanceof Resource) {
                System.out.print(object.toString());
            } else {
                // object is a literal
                System.out.print(" \"" + object.toString() + "\"");
            }

            System.out.println(" .");
        }
    }
}